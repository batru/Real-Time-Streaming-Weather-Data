import requests
import pandas as pd
import json
from dotenv import load_dotenv
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv() # Load env 
uri = os.getenv('DB_STRING')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


def extract_data():


    city_name = 'Nairobi'

    # get API KEY
    KEY = os.getenv('WEATHER_KEY')

    #load weeather data in Mombasa,KE from openweathermap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={KEY}"


    weather_data = requests.get(url=url)

    df_weather = pd.DataFrame(weather_data.json()['weather'], index=[1])
    df_temp = pd.DataFrame(weather_data.json()['main'], index=[1])

    country = weather_data.json()['sys']['country']

    df_loc = pd.DataFrame(
        {
            'country': country,
            'city': city_name
        },
        index=[1]
    )

    #merge data frame
    merged_df = pd.merge(pd.merge(df_weather, df_temp, left_index=True, right_index=True, how='outer'),
                        df_loc, left_index=True, right_index=True, how='outer'
                        )
    return merged_df
def transform_data(merged_df):
    # drop columns 
    df = merged_df.drop(columns=['id', 'icon'])

    #tranform temp from kelvin to celcius
    temp_list = ['temp', 'feels_like', 'temp_min', 'temp_max']

    df[temp_list] = df[temp_list] - 273

    data_dict = df.to_dict(orient="records") #Convert the DataFrame to a list of dictionaries

    return data_dict


def load_data(data_dict):

    #load to mongodb

    db = client['weather_db']  #create db 
    collection = db['weather_data'] #creates collection


    # data_dict = df.to_dict(orient="records") #Convert the DataFrame to a list of dictionaries

    # print(data_dict)

    collection.insert_many(data_dict) # insert the entire DataFrame into the collection

