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
        payload = {"email" : "kii1u20@soton.ac.uk", "oldPassword" : "testPassword", "newPassword" : "testPassword" }

        resp = requests.get(
                'http://localhost:7071/api/user/updatePassword', 
                json = payload)


        self.assertEqual({"result" : True, 'message' : 'OK'}, resp.json())

    def test_wrongPassword(self):
        payload = {"email" : "kii1u20@soton.ac.uk", "oldPassword" : "12345678", "newPassword" : "testPassword" }

        resp = requests.get(
                'http://localhost:7071/api/user/updatePassword', 
                json = payload)


        self.assertEqual({"result": False , "message": "Incorrect credentials."}, resp.json())

    def test_wrongEmail(self):
        payload = {"email" : "kii1u20@ston.uk", "oldPassword" : "testPassword", "newPassword" : "testPassword" }

        resp = requests.get(
                'http://localhost:7071/api/user/updatePassword', 
                json = payload)


        self.assertEqual({"result": False , "message": "The email does not exist in the database."}, resp.json())

    def test_shortPassword(self):
        payload = {"email" : "kii1u20@soton.ac.uk", "oldPassword" : "testPassword", "newPassword" : "t" }

        resp = requests.get(
                'http://localhost:7071/api/user/updatePassword', 
                json = payload)


        self.assertEqual({"result": False, "message": "The password should be between 6 and 18 characters inclusive."}, resp.json())

    def test_longPassword(self):
        payload = {"email" : "kii1u20@soton.ac.uk", "oldPassword" : "testPassword", "newPassword" : "123456789123456789123456789" }

        resp = requests.get(
                'http://localhost:7071/api/user/updatePassword', 
                json = payload)


        self.assertEqual({"result": False, "message": "The password should be between 6 and 18 characters inclusive."}, resp.json())