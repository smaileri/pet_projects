from flask import Flask, render_template, request
import requests
from src.utils import url_search, extract_links

app = Flask(__name__)

@app.route('/')
def ask_search():
    return render_template("ask_search.html")

@app.route("/search")
def search():
    key_word = request.args.get("key_word")
    url = url_search(key_word)
    response = requests.get(url)
    links = extract_links(response)
    print(links)
    return render_template("show_gifs.html", search_content=key_word, link0=links[0], link1=links[1], link2=links[2])
    
app.run()