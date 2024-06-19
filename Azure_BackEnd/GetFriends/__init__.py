import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get friends list...')

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the user container
    users_container = database_client.get_container_client(config.settings['users_container'])

    user = req.get_json()

    email = user['email']
    password = user['password']
    

    try:
        # Search for the user
        results = list(users_container.query_items(query="SELECT users.friends FROM users WHERE users.email = @target1 AND users.password = @target2", parameters=[{"name": "@target1", "value": email}, {"name": "@target2", "value": password}], enable_cross_partition_query=True))
        
        #Should we return error or empty list when there is no friends?? Right now it returns empty list
        if(len(results) == 0):
           return func.HttpResponse(body = json.dumps({"result": False, "message": "No matches in the database." }), status_code=400)
        return func.HttpResponse(body = json.dumps(results[0]['friends']), status_code=200)
    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)