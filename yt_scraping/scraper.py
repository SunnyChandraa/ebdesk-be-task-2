import requests, sys, time, os, argparse
from insert_data import insert_data

snippet_data = ["channelId",
                "title",
                "channelTitle",
                "publishedAt"]

# Any characters to exclude
unsafe_characters = ['\n', '"']

# Identify column
header = snippet_data

# Get api key and country codes from file
def setup(api_path, code_path):
    with open(api_path, 'r') as file:
        api_key = file.readline()

    with open(code_path) as file:
        country_codes = [x.rstrip() for x in file]

    return api_key, country_codes


# Removes any character from the unsafe characters
def prepare_data(data):
    for char in unsafe_characters:
        data = str(data).replace(char, '')
    return f'"{data}"'



def api_request(page_token, country_code):
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=30&key={api_key}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temporary banned, please wait and try again later.")
        sys.exit()
    return request.json()


def get_videos(items):
    lines = []

    for video in items:

        # Snippet containing the most useful info
        snippet = video['snippet']

        # This list contains all of the features in snippet
        data = [prepare_data(snippet.get(data, "")) for data in snippet_data]

        line = data
        lines.append(",".join(line))


    return lines


def get_pages(country_code, next_page_token="&"):
    country_data = []

    while next_page_token is not None:
        # A Page of data contains all of the videos
        video_data_page = api_request(next_page_token, country_code)

        # Get the next page token and build a string which can be injected into the request with it
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token

        # Get all of the items as a list and let get_videos return the needed features
        items = video_data_page.get('items', [])
        country_data += get_videos(items)

    return country_data


# Write into csv
def write_to_file(country_code, country_data):

    print(f"Writing {country_code} data to file...")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f"{output_dir}/{time.strftime('%y.%d.%m')}_{country_code}_videos.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")


def save_data_as_file():
    for country_code in country_codes:
        country_data = [",".join(header)] + get_pages(country_code)
        write_to_file(country_code, country_data)

def save_data_to_db():
    for country_code in country_codes:
        country_data = get_pages(country_code)

        for c_data in country_data:
            insert_data(c_data.split('",')[0].replace('"', ''),
                        c_data.split('",')[1].replace('"',''),
                        c_data.split('",')[-2].replace('"',''),
                        c_data.split('",')[-1].replace('"',''))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path', help='Path to the file containing the api key', default='api_key.txt')
    parser.add_argument('--country_code_path', help='Path to the file containing the list of country codes to scraped', default='country_codes.txt')
    parser.add_argument('--output_dir', help='Path to save the outputted files in', default='output/')

    args = parser.parse_args()

    output_dir = args.output_dir
    api_key, country_codes = setup(args.key_path, args.country_code_path)

    #save data into db and file
    save_data_to_db()
    save_data_as_file()