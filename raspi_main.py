from database_management import Cosmos_DB
import datetime
import time
from oled_util import OLED
import joystick_util as joy

print("Initializing cosmos db ...")
cosmos = Cosmos_DB()
print("Succesfully connected to cosmos db ...")
oled = OLED()

def swipe_screen(data_list):
    """
    display guage data according to chosen index
    :param data: list of tuples [(Title, value, unit), (Title, value, unit), ...]
    """
    global index
    oled.write_gauge(data_list[index][0], data_list[index][1], data_list[index][2])

def get_data():
    
    print("Data updated at {}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
    # get data from cosmos
    data = {}
    for item in cosmos.query_item('4001'):
        #print(item)
        data = item
    
    # create data list
    data_list = []
    
    data_list.append(("Trip Traveled", data['stat_data']['current_trip_mileage'], "m"))
    #print('Current Trip Mileage =',data['stat_data']['current_trip_mileage'])
    
    data_list.append(("Fuel Used", data['stat_data']['current_fuel']*0.01, "L"))
    #print('Current Fuel =',data['stat_data']['current_fuel'])

    utc_time = datetime.datetime.strptime(data['stat_data']['UTC_Time'], '%Y-%m-%d %H:%M:%S')
    accon_time = datetime.datetime.strptime(data['stat_data']['last_accon_time'], '%Y-%m-%d %H:%M:%S')
    time_spent = utc_time-accon_time

    #print('UTC Time',utc_time)
    #print('Accon_time',accon_time)

    data_list.append(("Time Spent", time_spent, "s"))
    #print('Time Spent',time_spent)
    
    return data_list

def increase_index():
    global index, selected_data
    if index + 1 <= len(selected_data) - 1:
        index += 1
    # return to first position
    else:
        index = 0
def decrease_index():
    global index, selected_data
    if index - 1 >= 0:
        index -= 1
    # return to last position
    else:
        index = len(selected_data) -1

if __name__ == "__main__":
    
    lap_start = time.time()
    selected_data = get_data()
    index = 0
    joy.left.when_pressed = decrease_index
    joy.right.when_pressed = increase_index
    
    while True:
        
        lap_end = time.time()
        if round(lap_end - lap_start) >= 10:
            # update data
            selected_data = get_data()
            lap_start = lap_end
            
        swipe_screen(selected_data)

    
    
