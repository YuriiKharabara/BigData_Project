from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp, window, count, coalesce, lit
from pyspark.sql.types import StructType, StringType

KEYSPACE = "pageinfo"

spark = SparkSession.builder \
    .appName("Spark Load to Multiple Cassandra Tables") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.cassandra.connection.port", "9042") \
    .getOrCreate()

json_schema = StructType() \
    .add("performer", StructType().add("user_id", StringType()).add("user_text", StringType())) \
    .add("meta", StructType().add("domain", StringType())) \
    .add("page_id", StringType()) \
    .add("rev_content_model", StringType()) \
    .add("rev_content_format", StringType()) \
    .add("comment", StringType()) \
    .add("page_title", StringType()) \
    .add("dt", StringType())

spark.sparkContext.setLogLevel('ERROR')

stream_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9093") \
    .option("subscribe", "input") \
    .option("startingOffsets", "earliest") \
    .load()

df = stream_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

parsed_df = df.select(from_json(col("value"), json_schema).alias("data")).select(
    col("data.performer.user_id").alias("user_id"),
    col("data.performer.user_text").alias("user_name"),
    col("data.rev_content_model").alias("content_model"),
    col("data.rev_content_format").alias("content_format"),
    col("data.meta.domain").alias("domain"),
    col("data.page_id").alias("page_id"),
    col("data.comment").alias("comment"),
    to_timestamp(col("data.dt"), "yyyy-MM-dd'T'HH:mm:ss'Z'").alias("created_at"),
    col("data.page_title").alias("title")
).filter(col("user_id").isNotNull())

filtered_df_console = parsed_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()


def write_to_cassandra(batch_df, batch_id):
    batch_df.select(
        "domain", "created_at", "page_id", "title"
    ).write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="pages_by_domain", keyspace=KEYSPACE) \
        .save()

    batch_df.select(
        "user_id", "created_at", "domain", "page_id", "title"
    ).write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="pages_by_user", keyspace=KEYSPACE) \
        .save()

    batch_df.select(
        "page_id", "comment", "content_format", "content_model", "created_at", "domain",
        "title", "user_id", "user_name"
    ).write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="page_details", keyspace=KEYSPACE) \
        .save()

    page_counts_df = batch_df \
        .groupBy(
        col("user_id"),
        window(col("created_at"), "1 hour")
    ).agg(
        count("page_id").alias("pages_count")
    ).select(
        col("user_id"),
        col("window.start").alias("period_start"),
        col("window.end").alias("period_end"),
        col("pages_count")
    )

    cassandra_df = spark.read \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="user_activity", keyspace=KEYSPACE) \
        .load()

    updated_df = page_counts_df.alias("new") \
        .join(cassandra_df.alias("old"), ["user_id", "period_start"], "left_outer") \
        .select(
        col("new.user_id"),
        col("new.period_start"),
        col("new.period_end"),
        (col("new.pages_count") + coalesce(col("old.pages_count"), lit(0))).alias("pages_count")
    )

    updated_df.select(
        "user_id", "period_start", "pages_count", "period_end"
    ).write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="user_activity", keyspace=KEYSPACE) \
        .save()


query = parsed_df.writeStream \
    .foreachBatch(write_to_cassandra) \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/spark-checkpoints-load-multiple-tables") \
    .start()

query.awaitTermination()
