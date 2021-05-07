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

tf_tables_list = ["1m", "6m", "15m", "1hr", "4hr", "1d"]

# def test_table_count():
#   "IF (SELECT COUNT(*)FROM information_schema.tables WHERE table_schema =  DATABASE() AND table_name = '1m')= 1 THEN RETURN TRUE; ELSE RETURN FALSE; END IF;"

def setup_tables():
    try: 
        print("Creating all tables: ")
        mycursor.execute("CREATE TABLE 1m (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_size DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
        mycursor.execute("CREATE TABLE 6m (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_size DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
        mycursor.execute("CREATE TABLE 15m (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_size DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
        mycursor.execute("CREATE TABLE 1hr (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_size DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
        mycursor.execute("CREATE TABLE 4hr (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_size DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
        mycursor.execute("CREATE TABLE 1d (frame INT, timestamp VARCHAR(32), pair VARCHAR(12), 21ema DECIMAL, 18ema DECIMAL, ema_trend VARCHAR(12), candle_open DECIMAL, candle_close DECIMAL, candle_high DECIMAL, candle_low DECIMAL, candle_size DECIMAL, candle_engulfing VARCHAR(8), vwap_mcb DECIMAL, vwap_mcb_trend VARCHAR(8), mfi_mcb DECIMAL, mfi_mcb_trend VARCHAR(8), big_green_dot_mcb VARCHAR(8), green_dot_mcb VARCHAR(8), red_dot_mcb VARCHAR(8), candle_strength_mcdbsi DECIMAL, candle_strength_mcdbsi_trend VARCHAR(8))")
        
        mycursor.execute("CREATE TABLE info (table_name VARCHAR(8), current_row_time INT(32))")

        mycursor.execute("INSERT INTO info () VALUES ('1m', 0)")
        mycursor.execute("INSERT INTO info () VALUES ('6m', 0)")
        mycursor.execute("INSERT INTO info () VALUES ('15m', 0)")
        mycursor.execute("INSERT INTO info () VALUES ('1hr', 0)")
        mycursor.execute("INSERT INTO info () VALUES ('4hr', 0)")
        mycursor.execute("INSERT INTO info () VALUES ('1d', 0)")

        db.commit()
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))

def remove_all_tables():
    try:
        print("removing all tables: ")
        mycursor.execute("DROP TABLE info")
        mycursor.execute("DROP TABLE 1m")
        mycursor.execute("DROP TABLE 6m")
        mycursor.execute("DROP TABLE 15m")
        mycursor.execute("DROP TABLE 1hr")
        mycursor.execute("DROP TABLE 4hr")
        mycursor.execute("DROP TABLE 1d")

    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))


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
def view_db_value(table_name, id_name, column_name):
    try: 
        query = "SELECT " + str(column_name) + " FROM " +str(table_name)+ " WHERE id = '" + str(id_name) + "'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        db.commit()
        return result[0][0]
    except mysql.connector.Error as error:
        print("Failed to retrieve record from database: {}".format(error))

def get_last_row_value(table_name, column_name):
    try: 
        query = "SELECT " +str(column_name)+ " FROM " +str(table_name)+ " ORDER BY timestamp DESC LIMIT 1"
        mycursor.execute(query)
        result = mycursor.fetchall()
        db.commit()
        return result[0][0]
    except mysql.connector.Error as error:
        print("Failed to retrieve record from database: {}".format(error))