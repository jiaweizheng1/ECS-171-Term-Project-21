from flask import Flask, request, render_template
import pickle
import numpy as np
import webbrowser as wb
from threading import Timer

app = Flask(__name__)

model1 = pickle.load(open('models/Regression_LinReg.pkl','rb'))

model2 = pickle.load(open('models/Regression_RF.pkl','rb'))

model3 = pickle.load(open('models/Classification_knn.pkl','rb'))

model4 = pickle.load(open('models/Classification_MLP.pkl','rb'))

model = ''

@app.route('/')
def init():
    return render_template('car_predict.html')

@app.route('/select_model', methods=['POST','GET'])
def select_model():
    global model 
    model = request.form.get('model', '')
    print(model)

    return render_template('car_predict.html', model = model)

@app.route('/predict1', methods=['POST','GET'])
def predict1():
    global model
    print(model)

    age = request.form.get("Age")
    owners = request.form.get("Number of Previous Owners")
    kms = request.form.get("Kms Driven")
    fuel = request.form.get("Fuel Type")
    seller_type = request.form.get("Seller Type")
    transmission = request.form.get("Transmission Type")

    age = (int(age))
    kms = np.log10(int(kms))
    if(int(owners) <= 1):
        owners = 0
    else:
        owners = 1
    fuel_Diesel = 1 if fuel.lower() == "diesel" else 0
    fuel_Petrol = 1 if fuel.lower() == "petrol" else 0
    seller_type_Dealer = 1 if seller_type.lower() == "dealer" else 0
    seller_type_Individual = 1 if seller_type.lower() == "individual" else 0
    transmission_Manual = 1 if transmission.lower() == "manual" else 0

    input_to_model = np.array([[age, kms, owners, fuel_Diesel, fuel_Petrol, seller_type_Dealer, seller_type_Individual, transmission_Manual]])

    if model == "1":
        prediction_logged = model1.predict(input_to_model)
    if model == "2":
        prediction_logged = model2.predict(input_to_model)
    
    return render_template('car_predict.html', pred = 'Predicted Price of Car is ${}.'.format(int(pow(10, prediction_logged))), model = model)
    
@app.route('/predict2', methods=['POST','GET'])
def predict2():
    global model
    print(model)

    age = request.form.get("Age")
    sell_price = request.form.get("Selling Price")
    kms = request.form.get("Kms Driven")
    fuel = request.form.get("Fuel Type")
    seller_type = request.form.get("Seller Type")
    transmission = request.form.get("Transmission Type")
    
    age = (int(age) - 10.527189265536723) / 4.366565310455436
    sell_price = (int(sell_price) - 463178.29996468924) / 535345.0704025673
    kms = (int(kms) - 70613.98181497175) / 46726.0783381431
    fuel_Diesel = 1 if fuel.lower() == "diesel" else 0
    fuel_Other = 1 if fuel.lower() == "other" else 0
    fuel_Petrol = 1 if fuel.lower() == "petrol" else 0
    seller_type_Dealer = 1 if seller_type.lower() == "dealer" else 0
    seller_type_Individual = 1 if seller_type.lower() == "individual" else 0
    transmission_Automatic = 1 if transmission.lower() == "automatic" else 0
    transmission_Manual = 1 if transmission.lower() == "manual" else 0

    input_to_model = np.array([[age, sell_price, kms, fuel_Diesel, fuel_Other, fuel_Petrol, seller_type_Dealer, seller_type_Individual, transmission_Automatic, transmission_Manual]])

    if model == "3":
        prediction_probs = model3.predict_proba(input_to_model)
    if model == "4":
        prediction_probs = model4.predict_proba(input_to_model)
    
    if(prediction_probs.argmax() + 1 == 1):
        return render_template('car_predict.html', pred = 'Predicted Number of Previous Owners is 1.\n Prediction Probabilities are {0}.'.format(prediction_probs), model = model)
    else:
        return render_template('car_predict.html', pred = 'Predicted Number of Previous Owners is 2 or more.\n Prediction Probabilities are {0}.'.format(prediction_probs), model = model)

if __name__ == '__main__':
    Timer(1, wb.open_new("http:localhost:5000/")).start()
    app.run(debug=False)
    # app.run(debug=True)
