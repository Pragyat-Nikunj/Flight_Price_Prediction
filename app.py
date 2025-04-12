from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
app = Flask(__name__)

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods = ['GET', 'POST'])
def predit_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
        airline = request.form.get('airline'),
        date = request.form.get('date'),
        source = request.form.get('source'),
        destination = request.form.get('destination'),
        dep_time = request.form.get('dep_time'),
        arrival_time = request.form.get('arrival_time'),
        duration = request.form.get('duration'),
        stops = request.form.get('stops'),
        add_info = request.form.get('add_info')
        ) 
        pred_df = data.get_data_as_data_frame()
        print(pred_df)
        
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        print(f"Prediction Results: {results}")
        return render_template('home.html', results = results[0])
     
        
if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)
