from flask import Flask, request, render_template, redirect, url_for
from src.data_collection import Participants, ApiFetch, Summoner
from src.data_analysis import Analytics
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash import dash_table
import plotly.express as px
from flask import send_from_directory

app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')
app.debug = True

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        summoner_name = request.form.get('summoner_name')
        return redirect(url_for('summoner_profile', summoner_name=summoner_name))
    return render_template('home.html')

@app.route('/player/<summoner_name>', methods=['GET', 'POST'])
def summoner_profile(summoner_name):

    if request.method == 'POST':
        summoner_name = request.form.get('summoner_name')


    api_fetch = ApiFetch(summoner_name)
    summoner_data = api_fetch.fetch_summoner_data()
    match_ids = api_fetch.fetch_match_ids(20)  
    match_details = [api_fetch.fetch_match_data(match_id) for match_id in match_ids]

    return render_template('player.html', summoner_data=summoner_data, match_details=match_details)

def serve_layout():
    api_fetch = ApiFetch('puoiaiolam')
    matchs = api_fetch.fetch_match_id()
    match_data = Analytics(api_fetch, matchs[0])
    df = match_data.match_df

    fig = px.bar(df, x='championName', y='kills')

    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name":i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
    ),
    dcc.Graph(
        id='graph',
        figure=fig
    )
])

@app.route('/<path:path>')
def send_img(path):
    return send_from_directory('static/images', path)

dash_app.layout = serve_layout

