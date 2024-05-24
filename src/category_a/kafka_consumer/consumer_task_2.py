import json
from datetime import datetime, timedelta

from cassandra.cluster import Cluster
from kafka import KafkaConsumer

from ..constants import *


def save_to_cassandra(time_start, time_end, domain_bot_counts):
    cluster = Cluster([CASSANDRA_HOSTS])
    session = cluster.connect(CASSANDRA_KEYSPACE)

    for domain, bot_count in domain_bot_counts.items():
        session.execute(
            f"INSERT INTO bot_stats (time_start, time_end, domain, created_by_bots) VALUES (%s, %s, %s, %s)",
            (time_start, time_end, domain, bot_count)
        )

    session.shutdown()
    cluster.shutdown()


def main():
    cluster = Cluster(CASSANDRA_HOSTS)
    session = cluster.connect(CASSANDRA_KEYSPACE)
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='group-consumer2',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    current_hour = datetime.utcnow().replace(second=0, microsecond=0)
    next_hour = current_hour + timedelta(minutes=5)
    domain_bot_counts = {}

    for message in consumer:
        message = message.value
        domain = message.get('meta', {}).get('domain', 'unknown')
        is_bot = message.get('performer', {}).get('user_is_bot', False)

        if is_bot:
            if domain not in domain_bot_counts:
                domain_bot_counts[domain] = 0
            domain_bot_counts[domain] += 1

        now = datetime.utcnow().replace(second=0, microsecond=0)

        if now >= next_hour:
            print(f"Saving bot data for {current_hour} to Cassandra")
            save_to_cassandra(current_hour, next_hour, domain_bot_counts)
            current_hour = next_hour
            next_hour = current_hour + timedelta(minutes=5)
            domain_bot_counts = {}


if __name__ == "__main__":
    main()