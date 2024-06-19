import azure.cosmos as cosmos

settings = {
    'local_URI':'http://localhost:7071/api/',
    'cloud_URI':'to be completed',
    'db_URI':'https://comp3207groupcourseworkdatabase.documents.azure.com:443/',
    'db_key':'NlUlcbWypVIgpbaZiv6lcAbfCSlJhrTrpzLb3HtVvulFpBfyQ9BtHQ0vcmUHmCC42TWU5aKkzIHsACDbgD6eLQ==',
    'db_id':'comp3207groupcourseworkdatabase',
    'users_container': 'users',
    'personal_calendar': 'personal_calendar',
    'events_container': 'events'
}

db_URI = settings['db_URI']
db_id = settings['db_id']
db_key = settings['db_key']

client = cosmos.cosmos_client.CosmosClient(db_URI, db_key)
db_client = client.get_database_client(db_id)
