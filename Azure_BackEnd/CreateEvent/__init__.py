import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import json
import uuid;

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the events container
    events_container = database_client.get_container_client(config.settings['events_container'])
    
    input = req.get_json()
    input['id'] = str(uuid.uuid4())
    startDate = input['startTimeFrame']
    endDate = input['endTimeFrame']
    input['finalStartTime'] = []
    input['finalEndTime'] = []
    input['suggestions'] = []
    input['usersVoted'] = []
    title = input['title']
    description = input['description']
    try:
        if((not has_x_days(startDate['month'], startDate['day'])) or startDate['hour'] > 24 or startDate['minutes'] > 60):
            return func.HttpResponse(body = json.dumps({"result" : False, "message": "Incorrect start date" }), status_code=200)
        elif ((not has_x_days(endDate['month'], endDate['day'])) or endDate['hour'] > 24 or endDate['minutes'] > 60):
            return func.HttpResponse(body = json.dumps({"result" : False, "message": "Incorrect end date" }), status_code=200)
        elif (len(title) == 0):
            return func.HttpResponse(body = json.dumps({"result" : False, "message": "Please input a title" }), status_code=200)
        elif (len(description) == 0):
            return func.HttpResponse(body = json.dumps({"result" : False, "message": "Please input a description" }), status_code=200)
        

        while(True) :
            getEntries = list(events_container.query_items(query= "SELECT * FROM events WHERE events.id = '{0}'".format(input['id']), 
                                    enable_cross_partition_query=True))
            if(len(getEntries) == 0):
                break
            else:
                input["id"] = str(uuid.uuid4())

        events_container.create_item(body=input)
        return func.HttpResponse(body = json.dumps({"result" : True, "message": input['id'] }), status_code=200)
    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)

def has_x_days(month, x):
    if month in [1, 3, 5, 7, 8, 10, 12] and x <= 31:
        return True
    elif month in [4, 6, 9, 11] and x <= 30:
        return True
    elif month == 2 and x <= 28: #Need to check if the month has 28 or 29 days
        return True
    else:
        return False