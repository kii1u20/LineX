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
    users_container = database_client.get_container_client(config.settings['users_container'])

    def test_correctInput(self):
        payload = {"email" : "kii1u20@soton.ac.uk", "eventID" : "2", "status" : "accept"}

        resp = requests.get(
                'http://localhost:7071/api/user/modifyActiveEvent', 
                json = payload)


        self.assertEqual({"result" : True, 'message' : 'OK'}, resp.json())