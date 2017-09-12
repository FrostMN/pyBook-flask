#from fileIO import getConfig
from media import Book
import requests, json

from config import config as conf
from default_conf import config as dconf

if conf == "":
    config = dconf
else:
    config = conf

#conf = getConfig()
apiKey = config['API_KEY']
apiUrl = str(config['API_URL']).replace("{{KEY}}", apiKey)

def getBook(isbn):
    r = requests.get(apiUrl + isbn).text
    print(r)
    r_json = json.loads(r)
    title = r_json['data'][0]['title']
    try:
        if "," in str(r_json['data'][0]['author_data'][0]['name']):
            author_fname = str(r_json['data'][0]['author_data'][0]['name']).split(',')[1].strip()
            author_lname = str(r_json['data'][0]['author_data'][0]['name']).split(',')[0]
        else:
            author_fname = str(r_json['data'][0]['author_data'][0]['name']).split(' ')[0]
            author_lname = str(r_json['data'][0]['author_data'][0]['name']).split(' ')[1]
    except:
        author_fname = str("")
        author_lname = str("")
    isbn10 = r_json['data'][0]['isbn10']
    isbn13 = r_json['data'][0]['isbn13']
    return Book(title, author_fname, author_lname, isbn10, isbn13)
