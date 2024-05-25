from dotenv import load_dotenv
import os


load_dotenv()


# Kafka configurations
KAFKA_BROKER = os.getenv('KAFKA_BROKER')
KAFKA_TOPIC = os.getenv('CONSUMER_TOPIC')

# Cassandra configurations
CASSANDRA_KEYSPACE = os.getenv('CASSANDRA_KEYSPACE')
CASSANDRA_HOSTS = os.getenv('CASSANDRA_HOSTS')
CASSANDRA_PORT = os.getenv('CASSANDRA_PORT')


URL = os.getenv('URL')
