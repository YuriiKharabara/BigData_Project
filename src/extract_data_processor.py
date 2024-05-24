import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.spark_config import create_spark_session
from config.kafka_config import KAFKA_TOPIC, KAFKA_BROKER
from config.cassandra_config import CASSANDRA_KEYSPACE, CASSANDRA_HOSTS
from cassandra.cluster import Cluster
from kafka import KafkaProducer, KafkaConsumer
import json
from datetime import datetime, timedelta

class ExtractDataProcessor:
    def __init__(self):
        self.spark = create_spark_session()
        self.kafka_topic = KAFKA_TOPIC
        self.kafka_broker = KAFKA_BROKER
        self.cassandra_keyspace = CASSANDRA_KEYSPACE
        self.cassandra_hosts = CASSANDRA_HOSTS

    def extract(self, category, question_number):
        if category == "A":
            if question_number == 1:
                self.precomputed_report_1()
            elif question_number == 2:
                self.precomputed_report_2()
            elif question_number == 3:
                self.precomputed_report_3()
        elif category == "B":
            if question_number == 1:
                self.ad_hoc_query_1()
            elif question_number == 2:
                self.ad_hoc_query_2()
            elif question_number == 3:
                self.ad_hoc_query_3()
            elif question_number == 4:
                self.ad_hoc_query_4()
            elif question_number == 5:
                self.ad_hoc_query_5()

    def precomputed_report_1(self, n):
        # end_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        end_time = datetime.utcnow().replace(second=0, microsecond=0)
        start_time = end_time - timedelta(minutes=n)

        df = self.spark.read \
            .format("org.apache.spark.sql.cassandra") \
            .options(table="hourly_stats", keyspace=self.cassandra_keyspace) \
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

    def precomputed_report_2(self):
        # Implementation for precomputed report 2
        pass

    def precomputed_report_3(self):
        # Implementation for precomputed report 3
        pass

    def ad_hoc_query_1(self):
        # Implementation for ad-hoc query 1
        pass

    def ad_hoc_query_2(self):
        # Implementation for ad-hoc query 2
        pass

    def ad_hoc_query_3(self):
        # Implementation for ad-hoc query 3
        pass

    def ad_hoc_query_4(self):
        # Implementation for ad-hoc query 4
        pass

    def ad_hoc_query_5(self):
        # Implementation for ad-hoc query 5
        pass


if __name__ == "__main__":
    processor = ExtractDataProcessor()
    report = processor.extract("A", 1, 60)  # Example for last 60 minutes
    print(report)