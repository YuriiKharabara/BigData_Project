from kafka import KafkaConsumer
import json
from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.kafka_config import KAFKA_TOPIC, KAFKA_BROKER
from src.cassandra_config import CASSANDRA_KEYSPACE, CASSANDRA_HOSTS

def save_to_cassandra(hour_start, hour_end, domain_counts):
    cluster = Cluster(CASSANDRA_HOSTS)
    session = cluster.connect(CASSANDRA_KEYSPACE)

    for domain, count in domain_counts.items():
        session.execute(
            "INSERT INTO hourly_stats (hour_start, hour_end, domain, page_count) VALUES (%s, %s, %s, %s)",
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
        group_id='group-consumer1',  # Unique group ID. This is used for each consumer receiving all the messages from the same topic.
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    next_hour = current_hour + timedelta(hours=1)
    domain_counts = {}

    for message in consumer:
        message = message.value
        domain = message.get('meta', {}).get('domain', 'unknown')
        
        if domain not in domain_counts:
            domain_counts[domain] = 0
        domain_counts[domain] += 1

        now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        
        if now >= next_hour:
            print(f"Consumer1: Saving data for {current_hour} to Cassandra")
            save_to_cassandra(current_hour, next_hour, domain_counts)
            current_hour = next_hour
            next_hour = current_hour + timedelta(hours=1)
            domain_counts = {}

if __name__ == "__main__":
    main()
