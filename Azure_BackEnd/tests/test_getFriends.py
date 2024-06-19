import unittest
import requests 
import config
import azure.cosmos as cosmos
import json;

class TestFunction(unittest.TestCase):

    # Proxy object for the Cosmos Database account
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Proxy object for the comp3207-groupcoursework-database Cosmos Database
    database_client = client.get_database_client(config.settings['db_id'])

    # Proxy object for the users container
    users_container = database_client.get_container_client(config.settings['users_container'])

    #change assertEqual first parameter depending on each case
    def test_getFriends(self):
        payload = {"email": "cc@yahoo.com" , "password" : "12345678"}


        resp = requests.get(
                'https://comp3207groupcoursework-function.azurewebsites.net/api/user/getfriends', 
                json = json.dumps(payload))
        self.assertEqual([], resp.json())