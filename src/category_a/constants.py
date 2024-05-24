from dotenv import load_dotenv
import os

load_dotenv()

# Kafka configurations
KAFKA_BROKER = os.getenv('KAFKA_BROKER')
CONSUMER_TOPIC = os.getenv('CONSUMER_TOPIC')
PRODUCER_TOPIC = os.getenv('PRODUCER_TOPIC')
