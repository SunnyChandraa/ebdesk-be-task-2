import mysql.connector
from yt_config import config
from mysql.connector import Error


def create_table():
    try:
        mySql_Create_Table_Query = """CREATE TABLE yt_trending ( 
                                 id int(11) NOT NULL AUTO_INCREMENT,
                                 channel_id varchar(255) NOT NULL,
                                 title varchar(255) UNIQUE NOT NULL,
                                 channel_name varchar(255) NOT NULL,
                                 published_at DATE NOT NULL,
                                 PRIMARY KEY (id)) """

        params = config()

        connect = mysql.connector.connect(**params)

        if connect.is_connected():
            cursor = connect.cursor()
            result = cursor.execute(mySql_Create_Table_Query)
            print("yt_trending Table created successfully ")

    except Error as error:
        print("Failed to create table in MySQL: {}".format(error))

    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    create_table()