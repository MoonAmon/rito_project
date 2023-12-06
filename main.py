from flask import Flask, request, render_template
from src.data_collection import ApiFetch, Match, Analytics
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    api_fetch = ApiFetch('RGAPI-0a0dfc77-970e-45ad-8ecf-63037fa1b2d6', 'suzuhatitor', 'psyko','YKfiig2deMN2x_h6ifhd6PhXDGCwhxlhxzqLv_I1Ca17pegJT3v39UIOF1lewJufghu5_pdRyH103g')
    match_id = api_fetch.fetch_match_id()
    match_obj = Analytics(api_fetch, match_id[0])
    df = match_obj.get_dataframe_match()
    df.plot(kind='bar', x='championName', y='kills')
    plt.savefig('static/images/barplot.png')
    df_html = df.to_html()
    matches = api_fetch.fetch_match_data(match_id[0])
    return render_template('home.html', match=matches['info'], table=df_html)

