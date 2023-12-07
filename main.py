from flask import Flask, request, render_template
from src.data_collection import Participants, ApiFetch
from src.data_analysis import Analytics
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = Flask(__name__)
dash_app = dash.Dash(server=app, routes_pathname_prefix='/dash/')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def home():
    """
    Renderiza a página inicial do aplicativo Flask.
    Coleta dados da partida, dados dos participantes e dados de análise.
    Retorna o template home.html renderizado com os dados da partida e uma tabela com os dados de análise.
    """
    api_fetch = ApiFetch('pineapplepie')
    match_id = api_fetch.fetch_match_id()
    participant_1 = Participants(api_fetch, match_id[0], 0)
    participant_1.fetch_champion_icon()
    match_obj = Analytics(api_fetch, match_id[0])
    df = match_obj.get_dataframe_match()
    df_html = df.to_html()
    matches = api_fetch.fetch_match_data(match_id[0])
    return render_template('home.html', match=matches['info'], table=df_html)

@app.route("/buscar", methods = ["GET", "post"])
def buscar():
    """
    Manipula a funcionalidade de busca.
    Obtém o nome do invocador dos dados do formulário.
    Coleta dados da partida com base no nome do invocador.
    Retorna o template home.html renderizado com os dados da partida.
    """
    summoners_name = request.form["summoners_name"]
    api_fetch = ApiFetch(summoners_name)

    match_id = api_fetch.fetch_match_id()
    matches = api_fetch.fetch_match_data(match_id[0])
    return render_template('home.html', match=matches['info'])

@app.route("/dash")
def render_dash_page():
    """
    Renderiza a página Dash.
    """
    return dash_app.index()

dash_app.layout = html.Div([
    dcc.Dropdown(
        id='summoner-dropdown',
        options=[{'label': i, 'value': i} for i in ['summoner1', 'summoner2', 'summoner3']],  # substitua pelos nomes dos invocadores desejados
        value='summoner1'
    ),
    html.Div(id='match-stats'),
    dcc.Graph(id='line-chart')
])

@dash_app.callback(
    [Output('match-stats', 'children'),
     Output('line-chart', 'figure')],
    [Input('summoner-dropdown', 'value')]
)
def update_output(summoner_name):
    """
    Atualiza a saída com base no nome do invocador selecionado.
    Coleta dados da partida e dados de análise com base no nome do invocador.
    Cria um gráfico de barras usando os dados de análise.
    Retorna as estatísticas atualizadas da partida e a figura do gráfico de barras.
    """
    api_fetch = ApiFetch(summoner_name)
    match_id = api_fetch.fetch_match_id()
    matches = api_fetch.fetch_match_data(match_id[0])
    match_obj = Analytics(api_fetch, match_id[0])
    df = match_obj.get_dataframe_match()
    
    figure = go.Figure()
    figure.add_trace(go.Bar(x=df['championName'], y=df['kills'], name='Kills'))
    
    return (html.Div([
        html.H3('Estatísticas da Partida'),
        html.P(f'Nome do Invocador: {summoner_name}'),
        html.P(f'ID da Partida: {match_id[0]}'),
        # adicione mais estatísticas aqui
    ]), figure)