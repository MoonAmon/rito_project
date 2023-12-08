from flask import Flask, request, render_template
from src.data_collection import Participants, ApiFetch, Match
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

@app.route('/')
def home():
    api_fetch = ApiFetch('pineapplepie')
    matchs = api_fetch.fetch_match_id()
    return render_template('home.html', matchs=matchs)

@app.route('/<match_id>')
def match_detail(match_id):
    api_fetch = ApiFetch('pineapplepie')
    participants = Participants(api_fetch, match_id, 0)
    participants.fetch_all_champion_icons()
    return render_template('match.html', participants=participants.participants)

@app.route('/dashboard/')
def render_dashboard():
    return dash_app.index()


def serve_layout():
    api_fetch = ApiFetch('pineapplepie')
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

