from kafka import KafkaConsumer
import json
from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.kafka_config import KAFKA_TOPIC, KAFKA_BROKER
from src.cassandra_config import CASSANDRA_KEYSPACE, CASSANDRA_HOSTS

def save_to_cassandra(user_stats, hour_start, hour_end):
    cluster = Cluster(CASSANDRA_HOSTS)
    session = cluster.connect(CASSANDRA_KEYSPACE)

    for user_id, stats in user_stats.items():
        for stat in stats:
            session.execute(
                "INSERT INTO user_stats (user_id, user_name, page_title, creation_time) VALUES (%s, %s, %s, %s)",
                (str(user_id), stat['user_name'], stat['page_title'], stat['creation_time'])
            )

    session.shutdown()
    cluster.shutdown()

def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='group-consumer3',  # Unique group ID. This is used for each consumer receiving all the messages from the same topic.
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    next_hour = current_hour + timedelta(hours=1)
    user_stats = {}

    for message in consumer:
        message = message.value
        user_id = message.get('performer', {}).get('user_id', 'unknown')
        user_name = message.get('performer', {}).get('user_text', 'unknown')
        page_title = message.get('page_title', 'unknown')
        creation_time = datetime.utcnow()

        if user_id not in user_stats:
            user_stats[user_id] = []

        user_stats[user_id].append({
            'user_name': user_name,
            'page_title': page_title,
            'creation_time': creation_time
        })

        now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        if now >= next_hour:
            print(f"Consumer3: Saving data for {current_hour} to {next_hour} to Cassandra")
            save_to_cassandra(user_stats, current_hour, next_hour)
            current_hour = next_hour
            next_hour = current_hour + timedelta(hours=1)
            user_stats = {}

if __name__ == "__main__":
    main()
