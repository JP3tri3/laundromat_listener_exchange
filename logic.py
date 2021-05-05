import time
import datetime
import json
import sql_connector as conn

def store_data(data):

    table_name = data['table_name']
    passphrase = data['passphrase']

    for key in data:
        if data[key] != "null" and data[key] != table_name and data[key] != passphrase:
            column_name = key
            value = data[key]
            time = add_row_from_time(table_name)
            conn.update_table_values(table_name, time, column_name, value)

def add_row_from_time(table_name):
    digit = ''
    frame = ''

    for x in table_name:
        if x.isdigit():
            digit += x
        else:
            frame += x

    current_row_time = conn.view_info_table_value(table_name)
    time = get_time()
    time_frame = int(time[frame])
    
    if (current_row_time) == 0:
        print('current_row_time = 0, creating new row')
        conn.set_info_table_value(table_name, time_frame)
    else:
        check_time = int(current_row_time) + int(digit)
        if (time_frame >= check_time):
            print(f'creating new row for {table_name} table')
            conn.add_new_row(table_name, current_row_time)
            conn.set_info_table_value(table_name, time_frame)
            current_row_time = time_frame

        else:
            print(f'current row time: {current_row_time} for {table_name} table')
            print(f'next time frame for updated values: {check_time} {frame}')

    return current_row_time

def get_time():
    
    # convert time from epoch: 
    seconds = round(time.time(), 0)
    mins = round(seconds / 60, 0)
    hour = round(mins / 60, 0)
    day = round(hour / 24, 0)

    kv = {}

    # # add to dict: 
    kv = {'time' : datetime.datetime.now(), 'd' : day, 'hr' : hour, 'm' : mins}

    return kv