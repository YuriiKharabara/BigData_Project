from dotenv import load_dotenv
import os

from pyspark.sql import SparkSession

load_dotenv()


def create_spark_session():
    return SparkSession.builder \
        .appName("Wikipedia Page Create Batch Processor") \
        .config("spark.cassandra.connection.host", "cassandra") \
        .getOrCreate()


# Kafka configurations
KAFKA_BROKER = os.getenv('KAFKA_BROKER')
KAFKA_TOPIC = os.getenv('CONSUMER_TOPIC')

# Cassandra configurations
CASSANDRA_KEYSPACE = os.getenv('CASSANDRA_KEYSPACE')
CASSANDRA_HOSTS = os.getenv('CASSANDRA_HOSTS')

SPARK_SESSION = create_spark_session()
