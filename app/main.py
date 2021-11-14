from flask import Flask , request ,redirect ,url_for , render_template
import datetime
import pickle
import pymongo
import configparser
import urllib.parse
import datetime
import certifi

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

app = Flask(__name__)
model = pickle.load(open('app/model.pkl', 'rb'))


collection = run_databse()


@app.route("/" , methods=['POST', 'GET'])
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # as model is depend on many variables
    # using sample data and getting only few values from user other are taken as default
    test_data = [3.000e+00, 1.000e+00, 0.000e+00, 1.000e+00, 0.000e+00, 2.000e+00, 0.000e+00,
                 8.860e+01, 1.688e+02, 6.410e+01, 4.880e+01, 2.548e+03, 0.000e+00, 2.000e+00,
                 1.300e+02, 5.000e+00, 3.470e+00, 2.680e+00, 9.000e+00, 1.110e+02, 5.000e+03,
                 2.100e+01, 2.700e+01, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,
                 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,
                 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,
                 0.000e+00, 0.000e+00, 0.000e+00]

    data_inp = list(request.form.values())
    if(data_inp[0] == 'front'):
        test_data[6] = 0
    else:
        test_data[6] = 1

    if (data_inp[1] == 'gas'):
        test_data[1] = 1
    else:
        test_data[1] = 0

    if (data_inp[2] == 'std'):
        test_data[1] = 0
    else:
        test_data[1] = 1

    brands =["alfa-romeo","audi","bmw","buick","chevrolet","dodge","honda","isuzu","jaguar","mazda","mercury","mitsubishi",
         "nissan","peugeot","porshe","renault","saab","subaru","toyota","volkswagen","volvo"]

    test_data[brands.index(data_inp[3]) + 23] = 1


    prediction = model.predict([test_data])[0].round(3)

    sample_data = {"fuletype": data_inp[1]  ,"enginelocation":data_inp[0],"aspiration":data_inp[2]}
    date_time = datetime.datetime.now().date()

    sample_data['date'] = (date_time.strftime("%d-%m-%Y"))
    sample_data['brand'] = data_inp[3]
    sample_data['price'] = prediction
    print(data_inp)

    print(sample_data)
    collection.insert_one(sample_data)

    return render_template('index.html', prediction_text='Cars price should be Rs {}'.format(prediction))

@app.route('/getData',methods=['POST','GET'])
def getData():
    return render_template('getData.html')

@app.route('/printData' ,methods=['POST' ,'GET'])
def printData():
    data_inp = list(request.form.values())
    print(data_inp)
    data = list(collection.find({'date': data_inp[0]}, {"_id": 0}))
    for line in data:
        print(line)
    if(len(data)==0):
        return render_template('nodata.html', date=data_inp[0])
    else:
        return render_template('displayData.html' , data = data)

if(__name__ == "__main__"):
    app.run(debug=False)