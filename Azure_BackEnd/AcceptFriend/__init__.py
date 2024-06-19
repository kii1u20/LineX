import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import json

import os
client = cosmos.cosmos_client.CosmosClient(os.environ['db_URI'], os.environ['db_key'])
db_client = client.get_database_client(os.environ['db_id'])
users_container = db_client.get_container_client(os.environ['users_container'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Accepting friend request')

    request = req.get_json()

    #the person trying to accept the request
    email_request = request['email1']
    password_email = request['password']
    #the person that sent the friend request
    email_pending = request['email2']

    if(email_request == email_pending):
        return func.HttpResponse(body = json.dumps({"result": False, "message": "You can't do actions for same emails" }), status_code=400) 

    try:
        #Search
        result1 = list(users_container.query_items(query="SELECT * FROM users WHERE users.email = @email_request", parameters=[{"name": "@email_request", "value": email_request}], enable_cross_partition_query=True))

        result2 = list(users_container.query_items(query="SELECT * FROM users WHERE users.email = @email_pending", parameters=[{"name": "@email_pending", "value": email_pending}], enable_cross_partition_query=True))

        if(len(result1) == 0):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "That email does not exist in the database" }), status_code=400)

        if(len(result2) == 0):
            #if email2 does not exist in db
            return func.HttpResponse(body = json.dumps({"result": False, "message": "The user you are trying to accept as a friend has not registered yet" }), status_code=400)

        #Test if the user making the request is logged in
        login = list(users_container.query_items(query="SELECT * FROM users WHERE users.email = @email_request AND users.password = @password", parameters=[{"name": "@email_request", "value": email_request}, {"name": "@password", "value": password_email}], enable_cross_partition_query=True))

        if(len(login) == 0):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "The email/password don't match" }), status_code=400)


        if(any(x['friend'] == email_pending and x['status'] == 'friend' for x in result1[0]['friends'])):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "You are already friend with this user" }), status_code=400)

        if(not any(x['friend'] == email_pending and x['status'] == 'request' for x in result1[0]['friends'])):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "There's not a request pending from this user" }), status_code=400)

        #accepting the friend request
        for friend in result1[0]['friends']:
            if friend['friend'] == email_pending:
                friend['status'] = 'friend'

        users_container.replace_item(result1[0]['id'], result1[0])
        
        for friend in result2[0]['friends']:
            if friend['friend'] == email_request:
                friend['status'] = 'friend'

        users_container.replace_item(result2[0]['id'], result2[0])

        return func.HttpResponse(body = json.dumps({"result": True, "message": "OK" }), status_code=200)

    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)