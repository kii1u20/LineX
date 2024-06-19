import unittest
import requests 
import config
import azure.cosmos as cosmos

class TestFunction(unittest.TestCase):

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the users container
    events_container = database_client.get_container_client(config.settings['events_container'])

    maxDiff = None

    def test_correctId(self):
        payload = {"id" : "a05563ba-707c-4bab-b099-bb8be503ef82", "finalStartTime": ["test"], "finalEndTime": ["test"]}

        resp = requests.get(
                'http://localhost:7071/api/SaveFinalEvent', 
                json = payload)

        self.assertEqual({"result" : True, "message" : "OK"}, resp.json())

    def test_infoIsSaved(self):
        payload = {"id" : "a05563ba-707c-4bab-b099-bb8be503ef82"}

        resp = requests.get(
                'http://localhost:7071/api/GetEvent', 
                json = payload)

        self.assertEqual({"result" : True, 'message' : {"users": ["kii1u20@soton.ac.uk", "dr5g20@soton.ac.uk"], "title": "Test event 1", "description": "Example description", "duration": {"day": 1}, "startTimeFrame": {"day": 22, "month": 12, "year": 2022, "hour": 13, "minutes": 30}, "endTimeFrame": {"day": 22, "month": 12, "year": 2022, "hour": 15, "minutes": 30}, "finalStartTime": ["test"], "finalEndTime": ["test"]}}, resp.json())

    def test_nonExistingId(self):
        payload = {"id" : "85613328-186b-4bc9-9adc-625c45364c6c", "finalStartTime": [], "finalEndTime": []}

        resp = requests.get(
                'http://localhost:7071/api/SaveFinalEvent', 
                json = payload)

        self.assertEqual({"result": False , "message": "This event doesn't exist"}, resp.json())