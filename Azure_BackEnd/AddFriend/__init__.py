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

    #the person sending friend request
    email1 = user['email1']
    password_email = user['password']
    #the person receiving invite
    email2 = user['email2']

    if(email1 == email2):
        return func.HttpResponse(body = json.dumps({"result": False, "message": "You can't do actions for same emails" }), status_code=400) 
    
    try:
        # Search 
        result1 = list(users_container.query_items(query="SELECT * FROM users WHERE users.email = @target1", parameters=[{"name": "@target1", "value": email1}], enable_cross_partition_query=True))
        result2 = list(users_container.query_items(query="SELECT * FROM users WHERE users.email = @target2", parameters=[{"name": "@target2", "value": email2}], enable_cross_partition_query=True))

        #Test if the user making the request is logged in
        login = list(users_container.query_items(query="SELECT * FROM users WHERE users.email = @email_request AND users.password = @password", parameters=[{"name": "@email_request", "value": email1}, {"name": "@password", "value": password_email}], enable_cross_partition_query=True))

        #if email1 does not exist in the db
        if (len(result1)==0):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "That email does not exist in the database" }), status_code=400)

        elif (len(result2)==0):
            #if email2 does not exist in db
            return func.HttpResponse(body = json.dumps({"result": False, "message": "The user you are trying to add as a friend has not registered yet" }), status_code=400)

        #user making the request is not logged in
        elif(len(login) == 0):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "The email/password don't match" }), status_code=400)
        
        #if users already are friends
        elif (any(x['friend'] == email2 for x in result1[0]['friends'])):
            return func.HttpResponse(body = json.dumps({"result": False, "message": "That user already is your friend or a request pending" }), status_code=400)

        else:
            answer1 = result1[0]
            answer1['friends'].append({'friend': email2, 'status': 'pending'})

            users_container.upsert_item(answer1)

            answer2 = result2[0]
            answer2['friends'].append({'friend': email1, 'status': 'request'})

            users_container.upsert_item(answer2)
            return func.HttpResponse(body = json.dumps({"result": True, "message": "OK" }), status_code=200)
    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)