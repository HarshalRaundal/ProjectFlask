import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import pickle


data = pd.read_csv("CarPrice_Assignment.csv")

# car_id is not revelent for model so dropping it
data.drop("car_ID" , axis=1 , inplace =True)

# correcting misspellings
data["car_brands"] = data['CarName'].str.split(' ' ,n=1, expand=True)[0]
data['car_brands'] = data['car_brands'].replace('alfa-romero', 'alfa-romeo')
data['car_brands'] = data['car_brands'].replace('maxda', 'mazda')
data['car_brands'] = data['car_brands'].replace('Nissan', 'nissan')
data['car_brands'] = data['car_brands'].replace('porcshce', 'porsche')
data['car_brands'] = data['car_brands'].replace('toyouta', 'toyota')
data['car_brands'] = data['car_brands'].replace(['vokswagen', 'vw'], 'volkswagen')
data.drop('CarName',axis=1,inplace=True)


#catogerical data to numerical for prediction using label encoding
le = LabelEncoder()

for col in data.select_dtypes(include=object):
    if col != 'car_brands':
        data[col] = le.fit_transform(data[col])

#carbrands data to numerical for prediction using one-hot encoding
data =pd.get_dummies(data , 'car_brands' ,drop_first=False)

#reordering price column as it is dependent variable

data_price = data['price']
data.drop('price',axis=1,inplace=True)
data['price']=data_price

# collecting x & y variables data
x = data.iloc[:,:-1].values
y = data.iloc[: ,-1].values

print(data.columns)
print(data.info())
x_sample = data.iloc[0 , :-1].values
print(x_sample)

#seperating training and testing data
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2,random_state=27)

# creating multiple linear regressor object
regressor = LinearRegression()

# taining model
regressor.fit(x_train, y_train)

#predicted on test data
y_pred = regressor.predict(x_test)


print("coeficient of determination : ",r2_score(y_test, y_pred))
# Got 92% score for model which is good enough to get idea about price of a car


# Saving model to disk
pickle.dump(regressor, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([x_sample]))

