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


def separate_tf(table_name):
    table_name_identifier = ''
    tf = ''
    attach = '_'

    i = 0
    for x in table_name:
        if (i == 0):
            if x != attach:
                table_name_identifier += x
            else:
                i += 1
        elif (i == 1):
            if x != attach:
                tf += x
    
    return tf

def add_row_from_time(table_name):
    tf = separate_tf(table_name)
    digit = ''
    frame = ''

    for x in tf:
        if x.isdigit():
            digit += x
        else:
            frame += x

    current_row_time = conn.view_info_table_value(table_name)
    time = get_time()
    time_frame = int(time[frame])
    check_time = int(current_row_time) + int(digit)

    if (current_row_time) == 0:
        print('current_row_time = 0, creating new row')
        conn.add_new_row(table_name, time_frame)
        conn.set_info_table_value(table_name, time_frame)
        current_row_time = time_frame
    else:
        if (time_frame >= check_time):
            print(f'creating new row for {table_name} table')
            conn.add_new_row(table_name, time_frame)
            conn.set_info_table_value(table_name, time_frame)
            current_row_time = time_frame

        else:
            print(f'current row time: {current_row_time} for {table_name} table')
            print(f'next time frame for creating new row: {check_time} {frame}')

    return current_row_time

def get_time():
    
    # convert time from epoch: 
    seconds = round(time.time(), 0)
    mins = round(seconds / 60, 0)
    hour = round(mins / 60, 0)
    day = round(hour / 24, 0)

    kv = {}

    # # add to dict: 
    kv = {'time' : datetime.datetime.now(), 'd' : day, 'h' : hour, 'hr' : hour, 'm' : mins}

    return kv


