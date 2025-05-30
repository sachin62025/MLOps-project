import joblib
import numpy as np
import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from flask import Flask, render_template, request

app = Flask(__name__)
logger = get_logger(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lead_time = request.form.get('lead_time', type=int)
        no_of_special_requests = request.form.get('no_of_special_requests', type=int)
        avg_price_per_room = request.form.get('avg_price_per_room', type=float)
        arrival_month = request.form.get('arrival_month', type=int)
        arrival_date = request.form.get('arrival_date', type=int)

        market_segment_type = request.form.get('market_segment_type')
        no_of_week_nights = request.form.get('no_of_week_nights', type=int)
        no_of_weekend_nights = request.form.get('no_of_weekend_nights', type=int)
        type_of_meal_plan = request.form.get('type_of_meal_plan')
        room_type_reserved = request.form.get('room_type_reserved')

        features = np.array([[
            lead_time,
            no_of_special_requests,
            avg_price_per_room,
            arrival_month,
            arrival_date,
            market_segment_type,
            no_of_week_nights,
            no_of_weekend_nights,
            type_of_meal_plan,
            room_type_reserved
        ]])
        
        prediction = loaded_model.predict(features)
        return render_template('index.html', prediction=prediction[0])
    return render_template('index.html', prediction=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)


