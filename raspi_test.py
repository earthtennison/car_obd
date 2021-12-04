from database_management import Cosmos_DB
import datetime
import time

cosmos = Cosmos_DB()
while(True):
    #print the last updated data in package 4002
    print(len(list(cosmos.query_item('4002'))))
    data = {}
    for item in cosmos.query_item('4002'):
        #print(item)
        data = item
    print('Current Trip Mileage =',data['stat_data']['current_trip_mileage'])
    print('Current Fuel =',data['stat_data']['current_fuel'])
    #print(type(data['stat_data']['UTC_Time']))

    utc_time = datetime.datetime.strptime(data['stat_data']['UTC_Time'], '%Y-%m-%d %H:%M:%S')
    accon_time = datetime.datetime.strptime(data['stat_data']['last_accon_time'], '%Y-%m-%d %H:%M:%S')
    time_spent = utc_time-accon_time

    print('UTC Time',utc_time)
    #print(type(utc_time))
    print('Accon_time',accon_time)
    #print(type(accon_time))

    print('Time Spent',time_spent)

    time.sleep(10)
    
    
