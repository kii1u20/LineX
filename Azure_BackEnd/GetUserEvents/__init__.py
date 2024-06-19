import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import json
import logging


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Getting user events...')

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])


    # Proxy object for the users container
    users_container = database_client.get_container_client(config.settings['users_container'])

    userInfo = req.get_json()

    email = userInfo['email']
    password = userInfo['password']
    
    try:
        # Search for the user
        results = list(users_container.query_items(query="SELECT * FROM users WHERE users.id = '{0}'".format(email), enable_cross_partition_query=True))
        if len(results) < 1:
            return func.HttpResponse(body=json.dumps({"result": False , "message": "No such user."}), status_code=400)
        elif (results[0]['email'] == email and results[0]['password'] == password):
            events = results[0]['activeEvents']
            return func.HttpResponse(body = json.dumps({"result" : True, "message": events }), status_code=200)
        else:
            return func.HttpResponse(body=json.dumps({"result": False , "message": "Incorrect credentials."}), status_code=400)
    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)