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
    events_container = database_client.get_container_client(config.settings['events_container'])

    def test_correctInput(self):
        payload = {"users" : ['kii1u20@soton.ac.uk'], 'title': 'Test event 1', 'description': 'Example description', 'duration' : {'hour' : 1}, 
                    'startTimeFrame' : {'day' : 22, 'month' : 12, 'year' : 2022, 'hour' : 13, 'minutes' : 30}, 
                    'endTimeFrame' : {'day' : 22, 'month' : 12, 'year' : 2022, 'hour' : 15, 'minutes' : 30}}

        resp = requests.get(
                'http://localhost:7071/api/events/createEvent', 
                json = payload)


        self.assertEqual({"result" : True, 'message' : resp.json()['message']}, resp.json())

    def test_incorrectStartDate(self):
        payload = {"users" : ['kii1u20@soton.ac.uk'], 'title': 'Test event 1', 'description': 'Example description', 'duration' : {'hour' : 1}, 
                    'startTimeFrame' : {'day' : 32, 'month' : 12, 'year' : 2022, 'hour' : 13, 'minutes' : 30}, 
                    'endTimeFrame' : {'day' : 22, 'month' : 12, 'year' : 2022, 'hour' : 15, 'minutes' : 30}}

        resp = requests.get(
                'http://localhost:7071/api/events/createEvent', 
                json = payload)


        self.assertEqual({"result" : False, "message": "Incorrect start date" }, resp.json())

    def test_incorrectEndDate(self):
        payload = {"users" : ['kii1u20@soton.ac.uk'], 'title': 'Test event 1', 'description': 'Example description', 'duration' : {'hour' : 1}, 
                    'startTimeFrame' : {'day' : 31, 'month' : 12, 'year' : 2022, 'hour' : 13, 'minutes' : 30}, 
                    'endTimeFrame' : {'day' : 31, 'month' : 6, 'year' : 2023, 'hour' : 15, 'minutes' : 30}}

        resp = requests.get(
                'http://localhost:7071/api/events/createEvent', 
                json = payload)


        self.assertEqual({"result" : False, "message": "Incorrect end date" }, resp.json())
