from flask import Flask, redirect, url_for, request, render_template
import os
import flask
import  numpy as np
# import pandas as pd
import pickle

app = Flask(__name__, template_folder='templates')

@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,3)
    print("inside valuepredictor")
    print("to_predict:",to_predict)
    model = pickle.load(open('kmeans_model.pkl', 'rb'))
    print("pickle file loaded")
    result = model.predict(to_predict)
    print("result:")
    return result[0]

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.values()
        print("form values:", to_predict_list)
        to_predict_list = list(map(float, to_predict_list))
        print("form values after list map:", to_predict_list)
        result = ValuePredictor(to_predict_list)
        print("result:", result)

        if float(result) == 0:
            prediction = 'Platinum'
        elif float(result) == 1:
            prediction = 'Gold'
        elif float(result) == 2:
            prediction = 'Silver'
        elif float(result) == 3:
            prediction = 'Bronze'
        
        return render_template("result.html", prediction=prediction)

if __name__== "__main__":
    app.run(debug=True)