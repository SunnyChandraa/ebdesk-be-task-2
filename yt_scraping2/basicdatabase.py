import sqlite3

conn = sqlite3.connect('lunch.db')
c = conn.cursor()

#delete table
#c.execute('''DROP TABLE meals''')

#create a table
c.execute("""CREATE TABLE youtube ( 
                                 id int(11) NOT NULL AUTO_INCREMENT,
                                 channel_id varchar(255) NOT NULL,
                                 title varchar(255) UNIQUE NOT NULL,
                                 channel_name varchar(255) NOT NULL,
                                 published_at DATE NOT NULL,
                                 PRIMARY KEY (id)) """)

#data to insert
def insert_data(channel_id, title, channel_tittle, published_at):
    params = config()
    connect = mysql.connector.connect(**params)

    try:

        mySql_insert_query = """INSERT INTO youtube (channel_id, title, channel_tittle, published_at) 
                            VALUES 
                            (%s, %s, %s, %s) """

        if connect.is_connected():
            cursor = connect.cursor()

            record = (channel_id, title, channel_tittle, published_at)
            cursor.execute(mySql_insert_query, record)
            connect.commit()
            print("Record inserting successfully into youtube table")

    except Error as error:
        print("Record inserted faile into youtube table {}".format(error))

    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()
            print("MySQL connection is closed")

#insert and commit to database
c.execute('''INSERT INTO youtube VALUES(?,?,?)''', (channel_id, tittle, channel_tittle, published_at))
conn.commit()

#select all data from table and print
c.execute('''SELECT * FROM youtube''')
results = c.fetchall()
print(results)

#close database connection
conn.close()
