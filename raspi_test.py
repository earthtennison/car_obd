from database_management import Cosmos_DB

cosmos = Cosmos_DB()
print(len(list(cosmos.query_item('4002'))))
#for item in cosmos.query_item('4002'):
    #print(item['stat_data'])
    
