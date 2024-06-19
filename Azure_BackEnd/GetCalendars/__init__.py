import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import json
import datetime
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the personal calendar container
    personal_calendar = database_client.get_container_client(config.settings['personal_calendar'])

    input = req.get_json()
    email = input['email']
    start_date = input['startDate']
    end_date = input['endDate']
    start_year = start_date['year']
    start_month = start_date['month']
    start_day = start_date['day']
    start_minutes = start_date['minutes']
    start_hour = start_date['hour']
    end_year = end_date['year']
    end_month = end_date['month']
    end_day = end_date['day']
    end_minutes = end_date['minutes']
    end_hour = end_date['hour']

    startDate = datetime.datetime(int(start_year), int(start_month), int(start_day), int(start_hour), int(start_minutes))
    endDate = datetime.datetime(int(end_year), int(end_month), int(end_day), int(end_hour), int(end_minutes))

    try:
        # Checking register errors
        getEntries = list(personal_calendar.query_items(query= "SELECT * FROM personal_calendar WHERE personal_calendar.email = '{0}'".format(email), 
                            enable_cross_partition_query=True))
        if(len(getEntries) == 0):
            return func.HttpResponse(body=json.dumps({"result": False , "message": "There aren't any calendars associated with this email."}), status_code=400)
        else:
            result = []
            for entry in getEntries:
                currentStartDate = entry['startDate']
                currentEndDate = entry['endDate']
                current_start_year = currentStartDate['year']
                current_start_month = currentStartDate['month']
                current_start_day = currentStartDate['day']
                current_start_minutes = currentStartDate['minutes']
                current_start_hour = currentStartDate['hour']
                current_end_year = currentEndDate['year']
                current_end_month = currentEndDate['month']
                current_end_day = currentEndDate['day']
                current_end_minutes = currentEndDate['minutes']
                current_end_hour = currentEndDate['hour']
                current_start_date = datetime.datetime(current_start_year, current_start_month, current_start_day, current_start_hour, current_start_minutes)
                current_end_date = datetime.datetime(current_end_year, current_end_month, current_end_day, current_end_hour, current_end_minutes)
                if((current_start_date>=startDate and current_start_date<=endDate) or (current_start_date<=startDate and current_end_date>=startDate)):
                    newEntry = {}
                    newEntry['email'] = entry['email']
                    newEntry['startDate'] = entry['startDate']
                    newEntry['endDate'] = entry['endDate']
                    newEntry['description']=entry['description']
                    result.append(newEntry)
            if len(result) == 0:
                return func.HttpResponse(body=json.dumps({"result": False , "message": []}), status_code=400)
            else:
                return func.HttpResponse(body = json.dumps({"result" : True, "message": result }), status_code=200)
    except exceptions.CosmosHttpResponseError as error:
         print(error.message)
         return func.HttpResponse("", status_code=404)
