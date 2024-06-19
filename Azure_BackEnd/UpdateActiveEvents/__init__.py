import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Logging in a user...')

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the user container
    users_container = database_client.get_container_client(config.settings['users_container'])

    user = req.get_json()
    email = user['email']
    eventID = user['eventID']
    status = user['status']

    try:
        # Checking register errors
        checkIfPresent = list(users_container.query_items(query= "SELECT * FROM users WHERE users.email = '{0}'".format(email), 
                            enable_cross_partition_query=True))
        if len(checkIfPresent) == 0:
            return func.HttpResponse(body=json.dumps({"result": False , "message": "The email does not exist in the database."}), status_code=400)
        else:
            if (eventID in checkIfPresent[0]['activeEvents'].keys()):
                return func.HttpResponse(body=json.dumps({"result": False , "message": "The user is already attending this event."}), status_code=400)
            else:
                checkIfPresent[0]['activeEvents'][eventID] = status
                users_container.upsert_item(body=checkIfPresent[0])
                return func.HttpResponse(body=json.dumps({"result": True , "message" : "OK"}), status_code=200)
    except exceptions.CosmosHttpResponseError as error:
            print(error.message)
            return func.HttpResponse("", status_code=404)
