import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import config


HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

class Cosmos_DB():

    def __init__(self,host,master_key,database_id,container_id):

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
    
    def read_item(self, doc_id):
        print('\nReading Item by Id\n')
        # Note that Reads require a partition key to be spcified.
        response = self.container.read_item(item=doc_id, partition_key=doc_id)
        print(response)
       


    def read_items(self):
        print('\nReading all items in a container\n')

        # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
        #       Important to handle throttles whenever you are doing operations such as this that might
        #       result in a 429 (throttled request)
        item_list = list(self.container.read_all_items(max_item_count=10))
        print('Found {0} items'.format(item_list.__len__()))
        for doc in item_list:
            print('Item Id: {0}'.format(doc.get('id')))
    
    def upsert_item(self,data):
        print('Upserting Items')  
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

