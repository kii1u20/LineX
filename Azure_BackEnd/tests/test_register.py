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

    def test_register(self):
        payload = {"name":  "TestName" , "password" : "TestPassword", "email" : "exampleEmail@example.com"}

        resp = requests.get(
                'http://localhost:7071/api/user/register', 
                json = payload)


        self.assertEqual({"result" : True, 'message' : 'OK'}, resp.json())

    def test_NonCompatiblePass(self):
        payload = {"name":  "TestName" , "password" : "Tesd", "email" : "exampleEmail@example.com"}

        resp = requests.get(
                'http://localhost:7071/api/user/register', 
                json = payload)


        self.assertEqual({"result" : False, 'message' : 'The password should be between 6 and 18 characters inclusive.'}, resp.json())

    def test_ExistingEmail(self):
        payload = {"name":  "TestName" , "password" : "TestPassword", "email" : "exampleEmail@example.com"}

        resp = requests.get(
                'http://localhost:7071/api/user/register', 
                json = payload)


        self.assertEqual({"result" : False, 'message' : 'The current email already exists in the database.'}, resp.json())