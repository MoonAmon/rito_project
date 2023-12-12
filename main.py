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

        return redirect(url_for('summoner_profile', summoner_name=summoner_name))
    # Pegando os dados do summoner
    summoner = Summoner(summoner_name)
    summoner_data = summoner.summoner_response
    tier, rank = summoner.fetch_rank()
    summoner_data['tier'] = tier
    summoner_data['rank'] = rank

    # Pegando as ultimas partidas do summoner
    #api_fetch = ApiFetch(summoner_name)
    #matchs_id = api_fetch.fetch_match_id(10)
    #matchs_data = api_fetch.fetch_all_match_data(matchs_id)

    return render_template('player.html', summoner_data=summoner_data)

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

