from flask import Flask, request, render_template
from src.data_collection import ApiFetch

app = Flask(__name__)

@app.route('/')
def home():
    api_fetch = ApiFetch('RGAPI-e028b775-f8aa-4754-a343-f798a9e72332', 'suzuhatitor', 'psyko')
    match_ids = api_fetch.fetch_match_id()
    matches = [api_fetch.fetch_match_data(match_id, 10) for match_id in match_ids]
    return render_template('home.html', matches=matches)