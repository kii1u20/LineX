import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Find Users...')

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the user container
    users_container = database_client.get_container_client(config.settings['users_container'])

    user = req.get_json()

    username = user['username']

    try:
        #right now when searching for empty string it will return empty list but this could later be changed to implement suggested friends
        if username=='':
            return func.HttpResponse(body = json.dumps([]), status_code=200)
            
        # Search for all usernames that contain this string user searching for, but ont return more than 10
        results = list(users_container.query_items(query="SELECT TOP 10 users.email, users.name FROM users WHERE CONTAINS (users.name, @target)", parameters=[{"name": "@target", "value": username}], enable_cross_partition_query=True))
             
        return func.HttpResponse(body = json.dumps(results), status_code=200)

    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)