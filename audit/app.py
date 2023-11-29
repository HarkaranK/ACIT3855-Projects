import connexion
from connexion import NoContent
from datetime import datetime
import os
import json
import uuid

#from SQLAlchemy import create_engine
#from sqlalchemy.orm import sessionmaker

from flask_cors import CORS, cross_origin

import yaml
import logging.config
import logging

from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yaml"
    log_conf_file = "/config/log_conf.yaml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yaml"
    log_conf_file = "log_conf.yaml"

with open('app_conf_file', 'r') as f:
    app_config = yaml.safe_load(f.read())

db_user = app_config['datastore']['user']
db_password = app_config['datastore']['password']
db_hostname = app_config['datastore']['hostname']
db_port = app_config['datastore']['port']
db_name = app_config['datastore']['db']

with open('log_conf_file', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)


REST_API = "./openapi.yaml"


def get_event_index(event_type, index):
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving {} at index {}".format(event_type, index))

    count = 0

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg_obj = json.loads(msg_str)
        if msg_obj.get('type') == event_type:
            if count == index:
                return msg_obj, 200
            else:
                count += 1

    logger.error("No more messages found")
    logger.error("Could not find {} at index {}".format(event_type, index))
    return {"message": "Not Found"}, 404


def get_weight_record_index(index):

    return get_event_index("add_weight", index)

def get_macros_record_index(index):
    
    return get_event_index("adding_macros", index)



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(REST_API, strict_validation=True, validate_responses=True )
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    app.run(port=8110)
