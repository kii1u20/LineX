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

    def test_login(self):
        payload = {"email": "kii1u20@soton.ac.uk" , "password" : "testPassword"}


        resp = requests.get(
                'http://localhost:7071/api/GetUserEvents', 
                json = payload)


        self.assertEqual({"result" : True, 'message' : {
        "1": "pending",
        "2": "pending"
    }}, resp.json())

    def test_IncorrectPass(self):
        payload = {"email": "example2@example.com" , "password" : "TestPassword3"}


        resp = requests.get(
                'http://localhost:7071/api/GetUserEvents', 
                json = payload)


        self.assertEqual({"result" : False, 'message' : 'Incorrect credentials.'}, resp.json())

    def test_NonExistingMail(self):
        payload = {"email": "exampl22eEmail@example.com" , "password" : "TestPassword3"}


        resp = requests.get(
                'http://localhost:7071/api/GetUserEvents', 
                json = payload)


        self.assertEqual({"result" : False, 'message' : 'No such user.'}, resp.json())