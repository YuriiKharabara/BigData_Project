import json
from datetime import datetime, timedelta

from cassandra.cluster import Cluster
from kafka import KafkaConsumer

from ..constants import *


def save_to_cassandra(hour_start, hour_end, domain_counts):
    cluster = Cluster([CASSANDRA_HOSTS])
    session = cluster.connect(CASSANDRA_KEYSPACE)

    for domain, count in domain_counts.items():
        session.execute(
            f"INSERT INTO hourly_stats (hour_start, hour_end, domain, page_count) VALUES (%s, %s, %s, %s)",
            (hour_start, hour_end, domain, count)
        )

    session.shutdown()
    cluster.shutdown()


def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='group-consumer1',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    current_hour = datetime.utcnow().replace(second=0, microsecond=0)
    next_hour = current_hour + timedelta(minutes=5)
    domain_counts = {}
    for message in consumer:
        message = message.value
        domain = message.get('meta', {}).get('domain', 'unknown')

        if domain not in domain_counts:
            domain_counts[domain] = 0
        domain_counts[domain] += 1

        now = datetime.utcnow().replace(second=0, microsecond=0)
        if now >= next_hour:
            print(f"Saving data for {current_hour} to Cassandra")
            save_to_cassandra(current_hour, next_hour, domain_counts)
            current_hour = next_hour
            next_hour = current_hour + timedelta(minutes=5)
            domain_counts = {}


if __name__ == "__main__":
    main()
