import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import config
import time


HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

class Cosmos_DB():

    def __init__(self,host=HOST,master_key=MASTER_KEY,database_id=DATABASE_ID,container_id=CONTAINER_ID):

        #Create Client
        self.client = cosmos_client.CosmosClient(host, {'masterKey': master_key} )

        # setup database 
        try:
            self.database = self.client.create_database(database_id)
        except exceptions.CosmosResourceExistsError:
            self.database = self.client.get_database_client(database_id)

        # setup container 
        try:
            self.container = self.database.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/package'))
        except exceptions.CosmosResourceExistsError:
            self.container = self.database.get_container_client(CONTAINER_ID)
        except exceptions.CosmosHttpResponseError:
            raise

    def query_item(self,package_num):
        query = 'SELECT TOP 1 * FROM c where c.package="{}" ORDER BY c.time DESC'.format(str(package_num))
        return self.container.query_items(query, enable_cross_partition_query=True) 
        
    def upsert_item(self,data):
        print('Upserting Items')
        data['time'] = time.time()
        self.container.upsert_item(body=data)
    
    def delete_item(self, doc_id,sql):
        #doc_id is the id of the data that you want to delete in the table, must be from the Partition Key table
        for item in self.container.query_items(
            query= sql,
            enable_cross_partition_query=True):
            self.container.delete_item(item, partition_key=doc_id)

def main():
    database = Cosmos_DB(HOST,MASTER_KEY,DATABASE_ID,CONTAINER_ID)
    # database.upsert_item({ 'id' : '1',
    #                     'last_accon_time': '2013-10-25 04:17:05',
    #                     'UTC_Time': '2013-10-25 04:18:05', 
    #                     'total_trip_mileage': 1151388, 
    #                     'current_trip_mileage': 0, 
    #                     'total_fuel': 33641, 
    #                     'current_fuel': 12, 
    #                     'vstate': '00000000', 
    #                     'reserved': '036401014C000300'})

if __name__ == '__main__':
    main()

