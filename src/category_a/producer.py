from kafka import KafkaProducer
import json
import requests
import time
from requests.exceptions import ChunkedEncodingError

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.kafka_config import KAFKA_TOPIC, KAFKA_BROKER

WIKI_STREAM_URL = "https://stream.wikimedia.org/v2/stream/page-create"

def send_to_kafka(producer, topic, message):
    producer.send(topic, value=message)
    producer.flush()

def main():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    while True:
        try:
            response = requests.get(WIKI_STREAM_URL, stream=True)

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data:'):
                        try:
                            message = json.loads(line[5:])
                            send_to_kafka(producer, KAFKA_TOPIC, message)
                        except json.JSONDecodeError:
                            continue
        except ChunkedEncodingError as e:
            print(f"Stream connection lost: {e}. Reconnecting...")
            time.sleep(5)  # wait for a short period before retrying
        except requests.RequestException as e:
            print(f"Request failed: {e}. Retrying...")
            time.sleep(1)  # wait for a short period before retrying

if __name__ == "__main__":
    main()
