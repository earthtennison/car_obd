import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://obd.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'whXTSvmqtQavVKAIOA3u98hekaI4tW77VjHXc16G9wFTIfYmYA8Osf59gL6aq748JmaWH0orZg5KdXc756c5Yg=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'obd_database'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'data'),
}