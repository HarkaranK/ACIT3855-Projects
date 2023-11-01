import connexion
from connexion import NoContent
from datetime import datetime
import os
import json
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

from add_macro import MacroRecord
from adding_weight import WeightRecord

import yaml
import logging.config
import logging

from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

db_user = app_config['datastore']['user']
db_password = app_config['datastore']['password']
db_hostname = app_config['datastore']['hostname']
db_port = app_config['datastore']['port']
db_name = app_config['datastore']['db']

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

# Logs Hostname
logger.info(f"Connected to MySQL database at {db_hostname}:{db_port}")

DB_ENGINE = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_hostname}:{db_port}/{db_name}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


REST_API = "./openapi.yaml"

def process_messages():
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])

    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
        reset_offset_on_start=False,
        auto_offset_reset=OffsetType.LATEST
    )

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)

        payload = msg["payload"]
        msg_type = msg["type"]

        session = DB_SESSION()

        if msg["type"] == "add_weight":

            weight_record = WeightRecord(weight=payload["weight"], note=payload["note"],trace_id=payload['trace_id'])
            session.add(weight_record)
            logger.info("Stored event add_weight request with a trace id of %s", payload['trace_id'])


        elif msg["type"] == "adding_macros": 

            macro_record = MacroRecord(
                protein=payload["protein"],
                carbohydrate=payload["carbohydrate"],
                fats=payload["fats"],
                vitamin_A=payload["vitamin_A"],
                vitamin_B=payload['vitamin_B'],
                vitamin_C=payload['vitamin_C'],
                vitamin_D=payload['vitamin_D'],
                vitamin_E=payload['vitamin_E'],
                vitamin_K=payload['vitamin_K'],
                calcium=payload['calcium'],
                sodium=payload['sodium'],
                iron=payload['iron'],
                potassium=payload['potassium'],
                magnesium=payload['magnesium'],
                zinc=payload['zinc'],
                omega_3=payload['omega_3'],
                omega_6=payload['omega_6'],
                trace_id=payload['trace_id']
                
            )
            session.add(macro_record)
            logger.info("Stored event adding_macros request with a trace id of %s", payload['trace_id'])

        session.commit()
        session.close()
        consumer.commit_offsets()


def get_weight(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(WeightRecord).filter(WeightRecord.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Weight Average readings after %s returned %d results" % (timestamp, len(results_list)))
    return results_list, 200


def get_macros(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(MacroRecord).filter(MacroRecord.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Macros readings after %s returned %d results" % (timestamp, len(results_list)))
    return results_list, 200



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(REST_API, strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    
    app.run(port=8091)