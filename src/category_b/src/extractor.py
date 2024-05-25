import json
import requests
from kafka import KafkaProducer
import logging
import constants

producer = KafkaProducer(bootstrap_servers=[constants.KAFKA_BROKER],
                         value_serializer=lambda m: json.dumps(m).encode('ascii'))


def send_messages():
    try:
        for line in requests.get(constants.URL, stream=True).iter_lines():
            if line:
                line = line.decode('utf-8').strip()
                if line.startswith('data:'):
                    json_str = line.split('data:', 1)[1].strip()
                    try:
                        event = json.loads(json_str)
                        logging.info(event)
                        producer.send(constants.KAFKA_TOPIC, event)
                        producer.flush()
                    except json.JSONDecodeError as e:
                        logging.info(f"Error decoding JSON: {e} - Line: {json_str}")
                    except Exception as e:
                        logging.info(f"An error occurred: {e}")
                else:
                    logging.info(f"Skipping non-data line: {line}")
    except Exception as e:
        send_messages()


if __name__ == "__main__":
    send_messages()
