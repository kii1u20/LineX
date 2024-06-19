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
        payload = {"email" : "kii1u20@soton.ac.uk", "eventID" : "1", "status" : "pending"}

        resp = requests.get(
                'http://localhost:7071/api/user/updateActiveEvents', 
                json = payload)


        self.assertEqual({"result" : True, 'message' : 'OK'}, resp.json())

    def test_wrongEmail(self):
        payload = {"email" : "kii1u20@ston.uk", "eventID" : "1", "status" : "pending"}

        resp = requests.get(
                'http://localhost:7071/api/user/updateActiveEvents', 
                json = payload)


        self.assertEqual({"result": False , "message": "The email does not exist in the database."}, resp.json())

    def test_shortPassword(self):
        payload = {"email" : "kii1u20@soton.ac.uk", "eventID" : "1", "status" : "pending"}

        resp = requests.get(
                'http://localhost:7071/api/user/updateActiveEvents', 
                json = payload)


        self.assertEqual({"result": False , "message": "The user is already attending this event."}, resp.json())