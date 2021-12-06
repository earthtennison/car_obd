from database_management import Cosmos_DB
import datetime
import time
from oled_util import OLED

print("Initializing cosmos db ...")
cosmos = Cosmos_DB()
print("Succesfully connected to cosmos db ...")
oled = OLED()

while(True):
    #print the last updated data in package 4001
    data = {}
    for item in cosmos.query_item('4001'):
        #print(item)
        data = item
        
    oled.write_gauge("Current Trip", data['stat_data']['current_trip_mileage'], "m")
    print('Current Trip Mileage =',data['stat_data']['current_trip_mileage'])
    
    time.sleep(2)
    
    oled.write_gauge("Current Fuel", data['stat_data']['current_fuel']*0.01, "L")
    print('Current Fuel =',data['stat_data']['current_fuel'])
    
    time.sleep(2)

    utc_time = datetime.datetime.strptime(data['stat_data']['UTC_Time'], '%Y-%m-%d %H:%M:%S')
    accon_time = datetime.datetime.strptime(data['stat_data']['last_accon_time'], '%Y-%m-%d %H:%M:%S')
    time_spent = utc_time-accon_time

    print('UTC Time',utc_time)
    print('Accon_time',accon_time)

    oled.write_gauge("Time Spent", time_spent, "s")
    print('Time Spent',time_spent)
    
    time.sleep(2)
    
    oled.clear()
    
    time.sleep(4)
    
    
