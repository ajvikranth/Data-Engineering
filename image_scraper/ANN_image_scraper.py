import requests
from bs4 import BeautifulSoup
import os, sqlite3



# Constants and Configuration
DB_FILE = "anime.db"
TABLE_NAME = "ANN_LINKS"

# Connect to the database
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Fetch all rows from the MYANIMELIST_LINKS table
cur.execute(f"SELECT * FROM {TABLE_NAME}")
rows = cur.fetchall()
rows_c = len(rows)
    
def imagedown(url):

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    images = soup.find_all('img')


    for image in images:

        if image['src'].split(".")[-1]=='jpg':

            print(image['src'])
            link = "https:"+image['src']

            name = str(id)


            with open(name + '.jpg', 'wb') as f:
                
                im = requests.get(link)
                print(im.status_code)
                f.write(im.content)

            print('Writing: ', name)



new_directory_name = "images"

img_dir_path = os.path.join(os.getcwd(),'data', new_directory_name)

# Join the current working directory with the new directory name
try:
    os.makedirs(img_dir_path)
except:    
    pass

os.chdir(img_dir_path)

id = 0

while id <  5:# rows_c:
    # Build the URL for the first request
    url = rows[id][1]
    imagedown(url)

    id+=1