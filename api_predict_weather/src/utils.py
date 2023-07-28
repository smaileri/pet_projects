from . import config 
from fuzzywuzzy import process
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def is_valid_city(city, cities):
    return city in cities

def closest_cities(city, cities, n_neighbors=3):
    neighbors = process.extract(query=city, choices=cities, limit=n_neighbors)
    return [name for name, score in neighbors]

def coordinates(city, df_cities):
    mask = df_cities['city']==city
    return df_cities[mask][['lat','lng']].values[0]

def create_link(city, df_cities):
    lat, lng = coordinates(city, df_cities)
    return config.METEO_LINK + f"latitude={lat}" + f"&longitude={lng}" + config.METEO_PARAMS

def create_prediction(response):
    #acces information in response
    data = pd.json_normalize( response.json())[["hourly.time",	"hourly.temperature_2m"]]
    data = data.explode(column=["hourly.time",	"hourly.temperature_2m"])
    
    data["hourly.time"] = data["hourly.time"].astype("datetime64")
    data["hourly.temperature_2m"] = data["hourly.temperature_2m"].astype(float)
    
    #creating wide-format data, that can be visialised
    data['hour'] = data["hourly.time"].dt.hour
    data['date'] = data["hourly.time"].dt.date
    df = data.pivot(index='hour', columns='date', values='hourly.temperature_2m')
    
    #create picture and save to folder
    sns.set_theme()
    plt.figure()
    sns.heatmap(df, cmap='vlag', annot=True)
    plt.xticks(rotation=45)
    plt.title('Prediction Weather')
    plt.tight_layout()
    plt.savefig('static/prediction.svg')

    