import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://obd.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'Mx0BLAvqO3Z9emsJIlC45B3pggYTOXUV5b8DCDOQUZMP4EE1XHBflxequToEG1VXb47JEpPumPisZTHLINABQQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'obd_database'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'data'),
}