import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Registering a user...')

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the user container
    users_container = database_client.get_container_client(config.settings['users_container'])

    user = req.get_json()

    password = user['password']
    email = user['email']
    user['id']=email
    user['friends'] = []
    user['activeEvents'] = {}

    try:
        # Checking register errors
        checkIfPresent = list(users_container.query_items(query=("SELECT * FROM users WHERE users.email = '{0}'".format(email)), enable_cross_partition_query=True))
        if(len(checkIfPresent) != 0):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "The current email already exists in the database." }), status_code=400)
        # todo - check if email is valid
        # elif(len(email) < 4 or len(username) > 10):
        #     return func.HttpResponse(body = json.dumps({"result": False, "message": "The username should be between 4 and 10 characters inclusive."}), status_code=400)
        elif(len(password) < 6 or len(password) > 18):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "The password should be between 6 and 18 characters inclusive."}), status_code=400)

        # Registering the user to the database
        users_container.create_item(body=user)
        return func.HttpResponse(body = json.dumps({"result" : True, "message": "OK" }), status_code=200)
    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)
