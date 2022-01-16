import csv
import googleapiclient.discovery

#create connection
conn = sqlite3.connect('cputest.db')
c = conn.cursor()

def most_popular(yt, **kwargs):
    popular = yt.videos().list(chart='mostPopular', part='snippet', **kwargs).execute()
    for video in popular['items']:
        yield video['snippet']

yt = googleapiclient.discovery.build('youtube', 'v3', developerKey= ) #enter your developer key / api key from yotube developer account
with open('YouTube Trending Titles on 12-30-18.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['channel_id', 'tittle', 'channel_name', 'publish_date'])
    csv_writer.writerows(
        [snip['channel_id'], snip['tittle'], snip['channel_name'], snip['publish_date']]
        for snip in most_popular(yt, maxResults=20, regionCode= ) #enter your region code based your nation code
    )
 
most_popular('https://www.overclockers.co.uk/amd-ryzen-9-3900x-twelve-core-4.6ghz-socket-am4-processor-retail-cp-3b5-am.html')
conn.commit()
print('complete.')

#select all from table
c.execute('''SELECT * FROM prices''')
results = c.fetchall()
print(results)

#close connection
conn.close()
