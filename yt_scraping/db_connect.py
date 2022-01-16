import mysql.connector
from mysql.connector import Error
from yt_config import yt_config

# connect to database
def connect():
    try:
        # read connection parameters
        params = yt_config()

        # connect to db
        print('Connecting to postgresql database...')
        connect = mysql.connector.connect(**params)

        if connect.is_connected():
            # create cursor
            cursor = connect.cursor()

            db_info = connect.get_server_info()
            print('MySQL database version: ', db_info)

            cursor = connect.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to database: ", record)

    except Error as error:
        print(error)
    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()