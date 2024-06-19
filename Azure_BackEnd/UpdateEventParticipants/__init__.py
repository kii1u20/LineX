import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import json
import logging


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Updating event participants...')

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the events container
    events_container = database_client.get_container_client(config.settings['events_container'])

    event = req.get_json()

    eventId = event['id']
    eventParticipant = event['user']
    task = event['task']
    
    try:
        # Search for the event
        results = list(events_container.query_items(query="SELECT * FROM events WHERE events.id = '{0}'".format(eventId), enable_cross_partition_query=True))
        logging.info(len(results))
        if len(results)==0:
            return func.HttpResponse(body=json.dumps({"result": False , "message": "This event doesn't exist"}), status_code=400)
        else:
            if task == "remove":
                results[0]['users'].remove(eventParticipant)
                events_container.upsert_item(results[0])
                return func.HttpResponse(body=json.dumps({"result": True , "message": "OK"}), status_code=400)
            elif task == "add":
                results[0]['users'].append(eventParticipant)
                events_container.upsert_item(results[0])
                return func.HttpResponse(body=json.dumps({"result": True , "message": "OK"}), status_code=400)
            else:
                return func.HttpResponse(body=json.dumps({"result": False , "message": "Unrecognized command"}), status_code=400)
    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)