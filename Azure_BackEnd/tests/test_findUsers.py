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

    #change assertEqual first parameter depending on each case
    def test(self):
        payload = {"username": "doesnotexist"}


        resp = requests.get(
                'http://localhost:7071/api/user/findusers', 
                json = payload)


        self.assertEqual([], resp.json())

    def test2(self):
        payload = {"username": "ex"}


        resp = requests.get(
                'http://localhost:7071/api/user/findusers', 
                json = payload)


        self.assertEqual(1, len(list(resp.json())))
        self.assertEqual([{"name": "example1", "email": "example1@example.com"}], resp.json())

    def test3(self):
        payload = {"username": ""}


        resp = requests.get(
                'http://localhost:7071/api/user/findusers', 
                json = payload)


        self.assertEqual(0, len(list(resp.json())))
        self.assertEqual([], resp.json())