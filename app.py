"""
Permet l'affichage web des données scrapées
en utilisant Flask, MongoDB et ElasticSearch 
"""

from flask import Flask
from flask import request
from flask import render_template, render_template_string
from flask import flash, redirect, request, url_for

import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import json
import numpy as np

from bokeh.embed import json_item
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.resources import CDN
from jinja2 import Template
from bokeh.io import show, output_file
import os
from pymongo import MongoClient
from search_bar import SearchBar
from graphs import create_bargraph

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


LOCAL = True

es_client = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])

app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'



@app.route('/MusicSearch', methods=('GET', 'POST'))
def MusicSearch():
    """
    Création de la barre de recherche ainsi que de l'affichage des données, et affichage du bargraph
    """
    form = SearchBar()
    if form.validate_on_submit():
        return redirect('/information/'+form.typing.data)
    div, script = create_bargraph()
    
    ranks, albums, artists = create_table()

    return render_template('music_search.html', form=form, 
        the_div=div, the_script=script, ranks=ranks, albums=albums, artists=artists)



@app.route('/information/<search_word>')
def sucess(search_word):
    """
    Affichage des résultats de la recherche en fonction des artistes et albums.
    """
    df_billboard = pd.DataFrame(list(billboard_200.find()))
    df_billboard_clean = df_billboard.drop(labels='_id',axis='columns')
    documents = df_billboard_clean.fillna("").to_dict(orient="records")

    bulk(es_client, generate_data(documents))

    QUERY = {
      "query": {
        "multi_match" : {
          "query":    search_word,
          "fields": [ "artist", "album" ] 
        }
      }
    }
    #result=["bonjour","merci"]
    result = es_client.search(index="albms", body=QUERY)
    source = result["hits"]["hits"]

    seen = set()
    new_source = []
    for d in source:
        t = tuple(d["_source"].items())
        if t not in seen:
            seen.add(t)
            new_source.append(d)

    album = [elt['_source']['album'] for elt in new_source]
    artist = [elt['_source']['artist'] for elt in new_source]
    rank = [elt['_source']['rank'] for elt in new_source]
    peak = [elt['_source']['peak'] for elt in new_source]
    duration = [elt['_source']['duration'] for elt in new_source]
    last_week = [elt['_source']['last_week'] for elt in new_source]

    return render_template('results.html',albums=album,artists=artist,ranks=rank, peak=peak, duration=duration, last_week=last_week)

def generate_data(documents):
    """
    Génération des données cherchées
    """
    for docu in documents:
        yield {
            "_index": "albms",
            "_type": "album",
            "_source": {k:v if v else None for k,v in docu.items()},
        }
        
        
def create_bargraph():
    """
    Création d'un bargraph en utilisant create_bar_chart
    """
    output_file("templates/music_search.html")

    artist = billboard_200.aggregate([{"$group" : {"_id" : "$artist", "sum" : {"$sum" : 1}}}])
    artist = list(artist)
    artist = sorted(artist, key=lambda k: k["sum"], reverse=True)

    artists = []
    sums = []

    data = {"artist": [], "sum": []}

    for i in artist[:20]:
      data["artist"].append(str(i["_id"]))
      data["sum"].append(int(i["sum"]))

    hover = create_hover_tool()
    plot = create_bar_chart(data, "", "artist", "sum", hover)
    script, div = components(plot)

    return div, script

def create_table():
    """
    Création du tableau
    """
    output_file("templates/music_search.html")
    _items = billboard_200.find()
    items = []
    for item in _items:
        items.append(item)

    classement = list(items)

    ranks = []
    albums = []
    artists = []

    for i in classement[:20]:
        ranks.append(i["rank"])
        albums.append(i["album"])
        artists.append(i["artist"])

    return ranks, albums, artists


def create_hover_tool():
    """
    Création d'un hover sur le bargraph
    """
    hover_html = """
      <div>
        <span class="hover-tooltip">@sum albums</span>
      </div>
    """
    return HoverTool(tooltips=hover_html)
    return None

def create_bar_chart(data, title, x_name, y_name, hover_tool=None, width=1200, height=300):
    """
    Création d'un bargraph qui compte l'occurence du nombre d'album dans le top 200 (seules les 20 premieres valeurs sont affichées)
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color="#e8ddb5")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Number of albums"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.major_label_orientation = 1
    return plot


if __name__ == '__main__':
    print("Running...")
    app.run(debug=True, port=2746)
