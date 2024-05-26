import json
import time

import requests
from kafka import KafkaProducer
import logging
import constants

producer = KafkaProducer(bootstrap_servers=[constants.KAFKA_BROKER],
                         value_serializer=lambda m: json.dumps(m).encode('ascii'))


def send_messages():
    while True:
        try:
            for line in requests.get(constants.URL, stream=True).iter_lines():
                if line:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data:'):
                        json_str = line.split('data:', 1)[1].strip()
                        try:
                            event = json.loads(json_str)
                            logging.info(f"Sending event: {event}")
                            producer.send(constants.KAFKA_TOPIC, event)
                            producer.flush()
                        except json.JSONDecodeError as e:
                            logging.error(f"Error decoding JSON: {e} - Line: {json_str}")
                        except Exception as e:
                            logging.error(f"An error occurred: {e}")
                    else:
                        logging.info(f"Skipping non-data line: {line}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error with HTTP request: {e}")
            time.sleep(10)
        except Exception as e:
            logging.error(f"An unknown error occurred: {e}")
            time.sleep(10)


if __name__ == "__main__":
    send_messages()
