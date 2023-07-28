from flask import Flask, request, render_template
import pandas as pd
import requests
import src.utils as utils

df_cities = pd.read_csv("data/belgium_cities.csv")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("search.html")

@app.route("/search")
def search():
    city = request.args.get("key_city")
    if utils.is_valid_city(city, df_cities['city'].values):
        url = utils.create_link(city, df_cities)
        response = requests.get(url)
        utils.create_prediction(response)
        
        return render_template("show_weather.html", user_input=city)
    else:
        closest_cities = utils.closest_cities(city, df_cities['city'].values)
        suggestions = ', '.join(closest_cities)
        return render_template("wrong_city.html", users_input=city, suggestions=suggestions)
    
app.run()