from azure.cosmos import exceptions, CosmosClient, PartitionKey
import obd_decoder

# Initialize the Cosmos client
endpoint = "https://obd.documents.azure.com:443/"
key = 'whXTSvmqtQavVKAIOA3u98hekaI4tW77VjHXc16G9wFTIfYmYA8Osf59gL6aq748JmaWH0orZg5KdXc756c5Yg=='

# # <create_cosmos_client>
# client = CosmosClient(endpoint, key)
# # </create_cosmos_client>

# # Create a database
# # <create_database_if_not_exists>
# database_name = 'obd_database'
# database = client.create_database_if_not_exists(id=database_name)
# # </create_database_if_not_exists>

# # Create a container
# # Using a good partition key improves the performance of database operations.
# # <create_container_if_not_exists>
# container_name = 'stat_data'
# container = database.create_container_if_not_exists(
#     id=container_name, 
#     partition_key=PartitionKey(path="/UTC_TIME"),
#     offer_throughput=400
# )
# </create_container_if_not_exists>


# Add items to the container
data_items = [obd_decoder.get_stat_data()]

 # <create_item>
for item in data_items:
    container.create_item(body=item)
# </create_item>

# Read items (key value lookups by partition key and id, aka point reads)
# <read_item>
# for family in family_items_to_create:
#     item_response = container.read_item(item=family['id'], partition_key=family['lastName'])
#     request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
#     print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
# </read_item>

# Query these items using the SQL query syntax. 
# Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
# <query_items>
query = "SELECT * FROM c"

items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
# </query_items>

#Send Delete Receive, Class 