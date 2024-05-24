from pyspark.sql import SparkSession

def create_spark_session():
    return SparkSession.builder \
        .appName("Wikipedia Page Create Batch Processor") \
        .config("spark.cassandra.connection.host", "cassandra") \
        .getOrCreate()
