import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
from datetime import datetime
import re


class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self ,features):
        try:
            model_path = 'artifacts\model.pkl'
            preprocessor_path = 'artifacts\preprocessor.pkl'
            model = load_object(file_path = model_path)
            preprocessor = load_object(file_path = preprocessor_path)
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(self,
        airline: str,
        source: str,
        destination: str,
        stops: str,
        add_info: str,
        date: str,               
        dep_time: str,           
        arrival_time: str,      
        duration: str            
    ):
        self.airline = airline
        self.source = source
        self.destination = destination
        self.stops = stops
        self.add_info = add_info
        self.date = date
        self.dep_time = dep_time
        self.arrival_time = arrival_time
        self.duration = duration

    def get_data_as_data_frame(self):
        try:
            # Parse date
            journey_date = datetime.strptime(self.date, "%Y-%m-%d")
            day = journey_date.day
            month = journey_date.month
            year = journey_date.year

            # Parse times
            dep = datetime.strptime(self.dep_time, "%H:%M")
            dept_hour = dep.hour
            dept_minute = dep.minute

            arr = datetime.strptime(self.arrival_time, "%H:%M")
            arrival_hour = arr.hour
            arrival_minute = arr.minute

            # Parse duration
            h_match = re.search(r"(\d+)h", self.duration)
            m_match = re.search(r"(\d+)m", self.duration)
            hours = int(h_match.group(1)) if h_match else 0
            minutes = int(m_match.group(1)) if m_match else 0
            duration_minutes = hours * 60 + minutes

            # Stops mapping
            stop_mapping = {
                "non-stop": 0,
                "1 stop": 1,
                "2 stops": 2,
                "3 stops": 3,
                "4 stops": 4
            }
            total_stops = stop_mapping.get(self.stops.lower(), 0)

            # Final data dict
            custom_data_input_dict = {
                "Airline": [self.airline],
                "Source": [self.source],
                "Destination": [self.destination],
                "Total_Stops": [total_stops],
                "Additional_Info": [self.add_info],
                "Day": [day],
                "Month": [month],
                "Year": [year],
                "Arrival_hour": [arrival_hour],
                "Arrival_minutes": [arrival_minute],
                "Dept_hour": [dept_hour],
                "Dept_minutes": [dept_minute],
                "Duration_minutes": [duration_minutes]
            }

            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            raise CustomException(e, sys)
        