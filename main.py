from flask import Flask, request, render_template
from src.data_collection import ApiFetch

app = Flask(__name__)

@app.route('/')
def home():
    api_fetch = ApiFetch('RGAPI-0a0dfc77-970e-45ad-8ecf-63037fa1b2d6', 'suzuhatitor', 'psyko')
    match_id = api_fetch.fetch_match_id()
    print(match_id)
    matches = api_fetch.fetch_match_data(match_id[0])
    return render_template('home.html', matches=matches)
