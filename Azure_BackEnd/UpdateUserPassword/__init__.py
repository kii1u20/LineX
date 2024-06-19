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
    oldPassword = user['oldPassword']
    newPassword = user['newPassword']

    try:
        # Checking register errors
        checkIfPresent = list(users_container.query_items(query= "SELECT * FROM users WHERE users.email = '{0}'".format(email), 
                            enable_cross_partition_query=True))
        if len(checkIfPresent) == 0:
            return func.HttpResponse(body=json.dumps({"result": False , "message": "The email does not exist in the database."}), status_code=400)
        else:
            # Logging the user in
            if (checkIfPresent[0]['email'] == email and checkIfPresent[0]['password'] == oldPassword):
                if(len(newPassword) < 6 or len(newPassword) > 18):
                    return func.HttpResponse(body = json.dumps({"result": False, "message": "The password should be between 6 and 18 characters inclusive."}), status_code=400)

                checkIfPresent[0]['password'] = newPassword
                users_container.upsert_item(body=checkIfPresent[0])
                return func.HttpResponse(body=json.dumps({"result": True , "message" : "OK"}), status_code=200)
            else:
                # The credentials do not match the ones in the database
                return func.HttpResponse(body=json.dumps({"result": False , "message": "Incorrect credentials."}), status_code=400)
    except exceptions.CosmosHttpResponseError as error:
            print(error.message)
            return func.HttpResponse("", status_code=404)
