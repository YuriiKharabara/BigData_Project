from kafka import KafkaConsumer
import json
from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.kafka_config import KAFKA_TOPIC, KAFKA_BROKER
from src.cassandra_config import CASSANDRA_KEYSPACE, CASSANDRA_HOSTS

def save_to_cassandra(hour_start, hour_end, domain_bot_counts):
    cluster = Cluster(CASSANDRA_HOSTS)
    session = cluster.connect(CASSANDRA_KEYSPACE)

    for domain, bot_count in domain_bot_counts.items():
        session.execute(
            "INSERT INTO bot_stats (time_start, time_end, domain, created_by_bots) VALUES (%s, %s, %s, %s)",
            (hour_start, hour_end, domain, bot_count)
        )

    session.shutdown()
    cluster.shutdown()

def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='group-consumer2', # Unique group ID. This is used for each consumer receiving all the messages from the same topic.
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    next_hour = current_hour + timedelta(hours=1)
    domain_bot_counts = {}

    for message in consumer:
        message = message.value
        domain = message.get('meta', {}).get('domain', 'unknown')
        is_bot = message.get('performer', {}).get('user_is_bot', False)
        
        if is_bot:
            if domain not in domain_bot_counts:
                domain_bot_counts[domain] = 0
            domain_bot_counts[domain] += 1

        now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        
        if now >= next_hour:
            print(f"Consumer2: Saving bot data for {current_hour} to Cassandra")
            save_to_cassandra(current_hour, next_hour, domain_bot_counts)
            current_hour = next_hour
            next_hour = current_hour + timedelta(hours=1)
            domain_bot_counts = {}

if __name__ == "__main__":
    main()
