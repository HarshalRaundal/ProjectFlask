import pymongo
import configparser
import urllib.parse
import datetime
import certifi

admin_pass ='Pass@123'

def run_databse():
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://admin:"+urllib.parse.quote("Password")+"@cluster0.c6arp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())

        db = client.test
        db = client['user_input']
        db_col = db['input']

        data = list(db_col.find({}, {"_id": 0}))
        for line in data:
            print(line)

        return db_col
    except:
        print('error to connect to Database')

    finally:
        client.close()
