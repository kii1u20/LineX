import unittest
import requests 
import config
import azure.cosmos as cosmos

class TestFunction(unittest.TestCase):

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the personal calendar container
    personal_calendar = database_client.get_container_client(config.settings['personal_calendar'])

    def test_get_Calendars(self):
        payload = {"email":  "kii1u20@soton.ac.uk" , "startDate": 
        {"day": 22, "month": 12, "year": 2022, "hour": 13, "minutes": 30}, "endDate": 
        {"day": 24, "month": 12, "year": 2022, "hour": 13, "minutes": 30}}

        resp = requests.get(
                'http://localhost:7071/api/GetCalendars', 
                json = payload)


        self.assertEqual({"result" : True, 'message' : [{"email": "kii1u20@soton.ac.uk", "startDate": {"day": 22, "month": 12, "year": 2022, "hour": 13, "minutes": 30},"endDate": {"day": 22, "month": 12, "year": 2022, "hour": 13, "minutes": 30}, "description": "Test event"}]}, resp.json())

    def test_get_Calendars_NonExistingEmail(self):
        payload = {"email":  "test@soton.ac.uk" , "startDate": 
        {"day": 23, "month": 12, "year": 2022, "hour": 13, "minutes": 30}, "endDate": 
        {"day": 24, "month": 12, "year": 2022, "hour": 13, "minutes": 30}}

        resp = requests.get(
                'http://localhost:7071/api/GetCalendars', 
                json = payload)


        self.assertEqual({"result" : False, 'message' : "There aren't any calendars associated with this email."}, resp.json())