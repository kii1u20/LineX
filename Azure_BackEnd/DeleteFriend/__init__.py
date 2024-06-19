import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Deleting friend')

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'])

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the user container
    users_container = database_client.get_container_client(config.settings['users_container'])

    request = req.get_json()

    #the person sending the delete request
    email_request = request['email1']
    password_email = request['password']
    #the person who is sending it for
    email_friend = request['email2']

    if(email_request == email_friend):
        return func.HttpResponse(body = json.dumps({"result": False, "message": "You can't do actions for same emails" }), status_code=400) 

    try:
        #Search
        result1 = list(users_container.query_items(query="SELECT * FROM users WHERE users.email = @email_request", parameters=[{"name": "@email_request", "value": email_request}], enable_cross_partition_query=True))

        result2 = list(users_container.query_items(query="SELECT * FROM users WHERE users.email = @email_friend", parameters=[{"name": "@email_friend", "value": email_friend}], enable_cross_partition_query=True))

        if(len(result1) == 0):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "That email does not exist in the database" }), status_code=400)

        if(len(result2) == 0):
            #if email2 does not exist in db
            return func.HttpResponse(body = json.dumps({"result": False, "message": "The user you are trying to delete/cancel request has not registered yet" }), status_code=400)

        #Test if the user making the request is logged in
        login = list(users_container.query_items(query="SELECT * FROM users WHERE users.email = @email_request AND users.password = @password", parameters=[{"name": "@email_request", "value": email_request}, {"name": "@password", "value": password_email}], enable_cross_partition_query=True))

        if(len(login) == 0):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "The email/password don't match" }), status_code=400)

        if(not any(x['friend'] == email_friend for x in result1[0]['friends'])):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "There's not a friendship with this user or a request" }), status_code=400)

        #delete/cancel request the friend request
        result1[0]['friends'] = [friend for friend in result1[0]['friends'] if friend['friend'] != email_friend]

        users_container.replace_item(result1[0]['id'], result1[0])
        
        result2[0]['friends'] = [friend for friend in result2[0]['friends'] if friend['friend'] != email_request]

        users_container.replace_item(result2[0]['id'], result2[0])

        return func.HttpResponse(body = json.dumps({"result": True, "message": "OK" }), status_code=200)

    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)