import connexion
from connexion import NoContent
from datetime import datetime
import os
import json
import uuid
import requests

from flask_cors import CORS, cross_origin

import os.path
from apscheduler.schedulers.background import BackgroundScheduler

import yaml
import logging.config
import logging

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


REST_API = "./openapi.yaml"

def populate_stats():
    logger.info("Start Processing")
    
    filename = app_config['datastore']['filename']
    if not os.path.isfile(filename):
        current_stats = {
            "num_weight_readings": 0,
            "max_weight_readings": 0,
            "num_macro_readings": 0,
            "max_protein_readings": 0,
            "last_updated": "2000-01-01T00:00:00Z"
        }    
    else:
        with open(filename, 'r') as f:
            content = f.read()
            if content.strip(): 
                current_stats = json.loads(content)
            else:
                current_stats = {
                    "num_weight_readings": 0,
                    "max_weight_readings": 0,
                    "num_macro_readings": 0,
                    "max_protein_readings": 0, 
                    "last_updated": "2000-01-01T00:00:00Z"
                }

    weight_event_response = requests.get(f"{app_config['eventstore']['url']}/weight?timestamp={last_updated}&end_timestamp={current_timestamp}")
    macro_event_response = requests.get(f"{app_config['eventstore']['url']}/macro?timestamp={last_updated}&end_timestamp={current_timestamp}")

    if weight_event_response.status_code != 200:
        logger.error(f"Error fetching weight events: {weight_event_response.status_code}")
        weight_events = []
    else:
        weight_events = weight_event_response.json()
        logger.info(f"Received {len(weight_events)} new weight events")

    if macro_event_response.status_code != 200:
        logger.error(f"Error fetching macro events: {macro_event_response.status_code}")
        macro_events = []
    else:
        macro_events = macro_event_response.json()
        logger.info(f"Recevied {len(macro_events)} new macro events")

    current_stats['num_weight_readings'] += len(weight_events)
    current_stats['num_macro_readings'] += len(macro_events)


    if weight_events:
        current_max_weight = current_stats['max_weight_readings']
        for event in weight_events:
            weight_value = event.get("weight", 0)
            if weight_value > current_max_weight:
                current_max_weight = weight_value
        
        current_stats['max_weight_readings'] = current_max_weight


    if macro_events:
        current_max_protein = current_stats['max_protein_readings']
        for event in macro_events:
            protein_value = event.get("protein", 0)
            if protein_value > current_max_protein:
                current_max_protein = protein_value
        
        current_stats['max_protein_readings'] = current_max_protein

    current_stats["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")



    with open(filename, 'w') as f:
        json.dump(current_stats, f, indent=4)
    
    logger.debug(f"Updated stats: {current_stats}")
    logger.info("Finished Processing")


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    #sched = BackgroundScheduler(daemon=False)
    sched.add_job(populate_stats,
                 'interval',
                 seconds=app_config['scheduler']['period_sec'])
    sched.start()

def get_stats():
    logger.info("GET /stats request started")
    filename = app_config['datastore']['filename']

    if not os.path.isfile(filename):
        logger.error("Statistics do not exist")
        return {"message": "Statistics do not exist"}, 404
    else:
        with open(filename, 'r') as f:
            current_stats = json.load(f)
        
    
    logger.debug(f"Statistics: {current_stats}")
    logger.info("GET /stats request completed")
    return current_stats, 200




app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api(REST_API,
    strict_validation=True, 
    validate_responses=True )




if __name__ == "__main__":
# run our standalone gevent server
    init_scheduler()
    app.run(port=8100, use_reloader=False)
