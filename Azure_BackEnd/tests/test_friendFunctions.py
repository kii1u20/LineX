import unittest
import requests 
import config
import azure.cosmos as cosmos

# Proxy object for the Cosmos Database account
client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )
# Proxy object for the comp3207-groupcoursework-database Cosmos Database
database_client = client.get_database_client(config.settings['db_id'])
# Proxy object for the users container
users_container = database_client.get_container_client(config.settings['users_container'])

email_1 = "csc1u20@soton.ac.uk"
email_2 = "cc@yahoo.com"
password = "12345678"

payload_1 = {'email1': email_1, 'password': password, 'email2': email_2}
payload_2 = {'email1': email_2, 'password': password, 'email2': email_1}

payload_wrong_email_1 = {'email1': "a", 'password': password, 'email2': email_2}
payload_wrong_email_2 = {'email1': email_1, 'password': password, 'email2': "a"}

payload_wrong_password = {'email1': email_1, 'password': 'a', 'email2': email_2}

payload_same_email = {'email1': email_1, 'password': password, 'email2': email_1}

addFriend = 'http://localhost:7071/api/user/addfriend'
acceptFriend = 'http://localhost:7071/api/user/acceptfriend'
rejectFriend = 'http://localhost:7071/api/user/rejectfriend'
deleteFriend = 'http://localhost:7071/api/user/deletefriend'

functions = [addFriend, acceptFriend, rejectFriend, deleteFriend]

class TestFunction(unittest.TestCase):
    def test(self):
        #resp = requests.get(.Friend, json = payload)
        #self.assertEqual({}, resp.json())

        for func in functions:
            resp = requests.get(func, json= payload_wrong_email_1)
            self.assertEqual({'result': False, 'message': 'That email does not exist in the database'}, resp.json())

            resp = requests.get(func, json= payload_wrong_password)
            self.assertEqual({'result': False, 'message': "The email/password don't match"}, resp.json())

            resp = requests.get(func, json= payload_same_email)
            self.assertEqual({'result': False, 'message': "You can't do actions for same emails"}, resp.json())
    
        resp = requests.get(addFriend, json= payload_wrong_email_2)
        self.assertEqual({'result': False, 'message': 'The user you are trying to add as a friend has not registered yet'}, resp.json())

        resp = requests.get(acceptFriend, json= payload_wrong_email_2)
        self.assertEqual({'result': False, 'message': 'The user you are trying to accept as a friend has not registered yet'}, resp.json())

        resp = requests.get(rejectFriend, json= payload_wrong_email_2)
        self.assertEqual({'result': False, 'message': 'The user you are trying to reject as a friend has not registered yet'}, resp.json())

        resp = requests.get(deleteFriend, json= payload_wrong_email_2)
        self.assertEqual({'result': False, 'message': 'The user you are trying to delete/cancel request has not registered yet'}, resp.json())

        #add friend
        print("Adding friends")
        resp = requests.get(addFriend, json= payload_1)
        self.assertEqual({'result': True, 'message': 'OK'}, resp.json())

        resp = requests.get(addFriend, json= payload_2)
        self.assertEqual({'result': False, 'message': 'That user already is your friend or a request pending'}, resp.json())

        #accept friend
        resp = requests.get(acceptFriend, json= payload_2)
        self.assertEqual({'result': True, 'message': 'OK'}, resp.json())

        resp = requests.get(acceptFriend, json= payload_2)
        self.assertEqual({'result': False, 'message': 'You are already friend with this user'}, resp.json())

        requests.get(deleteFriend, json= payload_1)
        resp = requests.get(acceptFriend, json= payload_2)
        self.assertEqual({'result': False, 'message': "There's not a request pending from this user"}, resp.json())

        #reject friend
        requests.get(addFriend, json= payload_1)
        resp = requests.get(rejectFriend, json= payload_2)
        self.assertEqual({'result': True, 'message': 'OK'}, resp.json())

        resp = requests.get(rejectFriend, json= payload_2)
        self.assertEqual({'result': False, 'message': "There's not a request pending from this user"}, resp.json())

        requests.get(addFriend, json= payload_1)
        requests.get(acceptFriend, json= payload_2)
        resp = requests.get(rejectFriend, json= payload_2)
        self.assertEqual({'result': False, 'message': "You are friend with this user, maybe you'd like to remove them"}, resp.json())

        #delete friend
        resp = requests.get(deleteFriend, json= payload_1)
        self.assertEqual({'result': True, 'message': 'OK'}, resp.json())

        resp = requests.get(deleteFriend, json= payload_1)
        self.assertEqual({'result': False, 'message': "There's not a friendship with this user or a request"}, resp.json())





