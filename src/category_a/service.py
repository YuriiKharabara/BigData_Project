# from config.spark_config import create_spark_session
from constants import *
from datetime import datetime, timedelta


def get_statistics(n: int):
    end_time = datetime.utcnow().replace(second=0, microsecond=0)
    start_time = end_time - timedelta(minutes=n)

    df = SPARK_SESSION.read \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="hourly_stats", keyspace=CASSANDRA_KEYSPACE) \
        .load() \
        .filter((df["hour_start"] >= start_time) & (df["hour_end"] < end_time))

    result = df.groupBy("hour_start", "hour_end", "domain") \
        .sum("page_count") \
        .withColumnRenamed("sum(page_count)", "page_count")

    result = result.collect()

    report = []
    for row in result:
        report.append({
            "time_start": row["hour_start"],
            "time_end": row["hour_end"],
            "statistics": {row["domain"]: row["page_count"]}
        })

    return report


def get_last_n_hours_by_bots(n: int):
    pass


def get_top_users(n: int):
    pass
