import os, fileIO, secrets, apiCalls
from sqlCalls import CreateDB, addBook

## run this first to setup the program ##

config_file = "config.py"

## uncomment the following line to see the config file as written
#print(config_text)

## creates the config directory if it doesnt exist
#if not fileIO.directoryExists(pybook_config_dir):
#    print("Creating config directory")
#    fileIO.createDirectory(pybook_config_dir)
#else:
#    print("config directory alredy exixts")

## creates the config file if it doesnt exist
if not fileIO.fileExists(config_file):

    ## sets values to be used in the config file
    #api_key = input("What's your API_KEY for isbndb.com? ")
    flask_secret_key = secrets.token_hex(32)
    api_url = "http://isbndb.com/api/v2/json/{{KEY}}/book/"

    ## builds the string to be written in the config file
    config_text = """
config = {'API_URL': '{{api_url}}', 'API_KEY': '{{api_key}}', 'SECRET_KEY': '{{secret}}'}
    """
    config_text = config_text.replace('{{api_url}}', api_url)
    config_text = config_text.replace('{{api_key}}', api_key)
    config_text = config_text.replace('{{secret}}', flask_secret_key)

    print("creating config file.")
    fileIO.createConfig(config_text)
else:
    print("config file already exists.")

## created the sqlite db if it dosent exist
if not fileIO.fileExists("pyBook.db"):
    print("creating pyBook.db")
    CreateDB()
    ## Loads test data into db
    addBook(apiCalls.getBook('0380973464'))
    addBook(apiCalls.getBook('0316154695'))
    addBook(apiCalls.getBook('0330258648'))
else:
    print("pyBook.db already exists")
