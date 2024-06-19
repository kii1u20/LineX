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

    #make sure that example1 and example 2 aren't friends already in the db or a request is not pending
    def test_correct(self):
        payload = {"email1": "example1@example.com" , "password":"12345678","email2" : "example2@example.com"}
        resp = requests.get('http://localhost:7071/api/user/addfriend', json = payload)
        self.assertEqual({"result" : True, 'message' : 'OK'}, resp.json())

        payload = {"email2": "example1@example.com", "password":"12345678","email1": "example2@example.com"}
        resp = requests.get('http://localhost:7071/api/user/rejectfriend', json = payload)
        self.assertEqual({"result" : True, 'message' : 'OK'}, resp.json())

    """#make sure that in the database there's no relationship between the 2 emails
    def test_noRequest(self):
        payload = {"email2": "example1@example.com", "password":"12345678","email1": "example2@example.com"}
        resp = requests.get('http://localhost:7071/api/user/rejectfriend', json = payload)
        self.assertEqual({"result" : False, 'message' : "There's not a request pending from this user"}, resp.json())"""
