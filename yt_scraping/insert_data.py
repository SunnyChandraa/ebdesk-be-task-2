import mysql.connector
from mysql.connector import Error
from yt_config import config


def insert_data(channel_id, title, channel_tittle, published_at):
    params = config()
    connect = mysql.connector.connect(**params)

    try:

        mySql_insert_query = """INSERT INTO yt_trending (channel_id, title, channel_tittle, published_at) 
                            VALUES 
                            (%s, %s, %s, %s) """

        if connect.is_connected():
            cursor = connect.cursor()

            record = (channel_id, title, channel_tittle, published_at)
            cursor.execute(mySql_insert_query, record)
            connect.commit()
            print("Record inserting successfully into yt_trending table")

    except Error as error:
        print("Record inserted faile into yt_trending table {}".format(error))

    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()
            print("MySQL connection is closed")