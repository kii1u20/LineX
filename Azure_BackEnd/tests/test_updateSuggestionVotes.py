import unittest
import requests 
import config
import azure.cosmos as cosmos

class TestFunction(unittest.TestCase):

    maxDiff = None

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the users container
    events_container = database_client.get_container_client(config.settings['events_container'])

    def test_correctId(self):
        payload = {"id" : '078e9acb-ddf2-43cc-b6ff-07896a83d1bc', "suggestion": '8e012218-9353-4d88-a63a-cd1e5ae2fd02'}

        resp = requests.get(
                'http://localhost:7071/api/UpdateSuggestionVotes', 
                json = payload)


        self.assertEqual({"result" : True, 'message' : "OK"}, resp.json())

    def test_nonExistingId(self):
        payload = {"id" : "a05563ba-707c-4bab-b099-bb8be503ef8211", "suggestion": ''}

        resp = requests.get(
                'http://localhost:7071/api/UpdateSuggestionVotes', 
                json = payload)


        self.assertEqual({"result": False , "message": "This event doesn't exist"}, resp.json())