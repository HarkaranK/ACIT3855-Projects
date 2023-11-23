import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import uuid
import datetime
import json
from pykafka import KafkaClient
import time

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


REST_API = "./openapi.yaml"

def get_kafka():
    retry_count = 0
    max_retries = app_config['kafka']['max_retries']
    sleep_time = app_config['kafka']['retry_delay_sec']

    while retry_count < max_retries:
        try:
            logger.info(f"Trying to connect to Kafka, attempt {retry_count+1}")
            client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
            kafka_topic = client.topics[str.encode(app_config['events']['topic'])]
            producer = kafka_topic.get_sync_producer()
            logger.info("Connected to Kafka successfully")
            return client, producer
            
        except Exception as e:
            logger.error(f"Connection to Kafka failed: {str(e)}")
            time.sleep(sleep_time)
            retry_count += 1
    raise Exception("Failed to connect to Kafka after retries")

    client, producer = get_kafka()

def send_kafka(event_type, payload):
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    
    msg = {
        "type": event_type,
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": payload
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

def add_weight(body):

    trace_id = str(uuid.uuid4())
    logger.info(f"Received event add_weight request with a trace id of {trace_id}")
    
    body['trace_id'] = trace_id
    

    send_kafka("add_weight", body)
    logger.info(f"Pushed add_weight event to Kafka (Id: {trace_id})")

    return NoContent, 201

def adding_macros(body):

    trace_id = str(uuid.uuid4())
    logger.info(f"Received event add_macros request with a trace id of {trace_id}")

    body['trace_id'] = trace_id
    send_kafka("adding_macros", body)

    logger.info(f"Pushed adding_macro event to Kafka (Id: {trace_id})")
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(REST_API, strict_validation=True, validate_responses=True )

if __name__ == "__main__":
    app.run(port=8080)
