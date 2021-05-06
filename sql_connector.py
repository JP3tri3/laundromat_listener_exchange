import sys
sys.path.append("..")
import mysql.connector
import config
import datetime

db = mysql.connector.connect(
    host = config.host,
    user = config.user,
    passwd = config.passwd,
    auth_plugin = config.auth_plugin,
    database = config.database_name
)

mycursor = db.cursor()

# mycursor.execute("CREATE TABLE 6m (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_side DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
# mycursor.execute("CREATE TABLE 15m (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_side DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
# mycursor.execute("CREATE TABLE 1hr (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_side DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
# mycursor.execute("CREATE TABLE 4hr (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_side DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
# mycursor.execute("CREATE TABLE 1d (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_side DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
# mycursor.execute("CREATE TABLE info (table_name VARCHAR(8), current_row_time INT(32))")

# mycursor.execute("INSERT INTO info () VALUES ('6m', 0)")
# mycursor.execute("INSERT INTO info () VALUES ('15m', 0)")
# mycursor.execute("INSERT INTO info () VALUES ('1hr', 0)")
# mycursor.execute("INSERT INTO info () VALUES ('4hr', 0)")
# mycursor.execute("INSERT INTO info () VALUES ('1d', 0)")

# db.commit()

def add_new_row(table_name, time_frame):
    mycursor.execute("INSERT INTO " + str(table_name) + " () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (time_frame, datetime.datetime.now(), 'empty', 0.0, 0.0, 'empty', 0.0, 0.0, 0.0, 0.0, 0.0, 'empty', 0.0, 'empty', 0.0, 'empty', 'empty', 'empty', 'empty', 0.0, 'empty'))
    db.commit()

def update_table_values(table_name, tf, column_name, value):
    try:
        if (isinstance(value, str)):
            query = "UPDATE " +str(table_name)+ " SET " + str(column_name) + "='" + str(value) + "' WHERE frame = '" + str(tf) + "'"
        else:
            query = "UPDATE " +str(table_name)+ " SET " + str(column_name) + "=" + str(value) + " WHERE frame = '" + str(tf) + "'"
        print(query)
        mycursor.execute(query)
        db.commit()
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))

## View info table value
def view_info_table_value(table):
    try: 
        table_name = 'info'
        value = 'current_row_time'
        query = "SELECT " + str(value) + " FROM " +str(table_name)+ " WHERE table_name = '" + str(table) + "'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        db.commit()
        return result[0][0]
    except mysql.connector.Error as error:
        print("Failed to retrieve record from database: {}".format(error))

def set_info_table_value(table_frame, value):
    try:
        table_name = 'info'
        column_name = 'current_row_time'
        if (isinstance(value, str)):
            query = "UPDATE " +str(table_name)+ " SET " + str(column_name) + "='" + str(value) + "' WHERE table_name = '" + str(table_frame) + "'"
        else:
            query = "UPDATE " +str(table_name)+ " SET " + str(column_name) + "=" + str(value) + " WHERE table_name = '" + str(table_frame) + "'"
        print(query)
        mycursor.execute(query)
        db.commit()
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))

## View Value
def viewDbValue(table_name, id_name, column_name):
    try: 
        query = "SELECT " + str(column_name) + " FROM " +str(table_name)+ " WHERE id = '" + str(id_name) + "'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        db.commit()
        return result[0][0]
    except mysql.connector.Error as error:
        print("Failed to retrieve record from database: {}".format(error))
