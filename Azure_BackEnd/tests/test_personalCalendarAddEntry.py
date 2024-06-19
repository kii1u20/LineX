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
    personal_calendar = database_client.get_container_client(config.settings['personal_calendar'])

    def test_correctInput(self):
        payload = {"email" : "kii1u20@soton.ac.uk", 'startDate' : {'day' : 22, 'month' : 12, 'year' : 2022, 'hour' : 13, 'minutes' : 30}, 
                    'endDate' : {'day' : 22, 'month' : 12, 'year' : 2022, 'hour' : 13, 'minutes' : 30}, 'description' : "Test event"}

        resp = requests.get(
                'http://localhost:7071/api/personalCalendar/addEvent', 
                json = payload)


        self.assertEqual({"result" : True, 'message' : 'OK'}, resp.json())

    def test_wrongStartDate(self):
        payload = {"email" : "kii1u20@soton.ac.uk", 'startDate' : {'day' : 32, 'month' : 12, 'year' : 2022, 'hour' : 13, 'minutes' : 30}, 
                    'endDate' : {'day' : 22, 'month' : 12, 'year' : 2022, 'hour' : 13, 'minutes' : 30}, 'description' : "Test event"}

        resp = requests.get(
                'http://localhost:7071/api/personalCalendar/addEvent', 
                json = payload)


        self.assertEqual({"result" : False, "message": "Incorrect start date" }, resp.json())


    def test_wrongEndDate(self):
        payload = {"email" : "kii1u20@soton.ac.uk", 'startDate' : {'day' : 22, 'month' : 12, 'year' : 2022, 'hour' : 13, 'minutes' : 30}, 
                    'endDate' : {'day' : 22, 'month' : 13, 'year' : 2022, 'hour' : 13, 'minutes' : 30}, 'description' : "Test event"}

        resp = requests.get(
                'http://localhost:7071/api/personalCalendar/addEvent', 
                json = payload)


        self.assertEqual({"result" : False, "message": "Incorrect end date" }, resp.json())