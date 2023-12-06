from flask import Flask, request, render_template
from src.data_collection import ApiFetch

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', match="Nenhum dado carregado")

@app.route("/buscar", methods = ["GET", "post"])
def buscar():
    summoners_name = request.form["summoners_name"]
    api_fetch = ApiFetch(summoners_name)
    
    match_id = api_fetch.fetch_match_id()
    matches = api_fetch.fetch_match_data(match_id[0])
    return render_template('home.html', match=matches['info'])
    
