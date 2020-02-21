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
from bokeh.plotting import figure
from bokeh.resources import CDN
from jinja2 import Template
from bokeh.io import show, output_file
import os
from pymongo import MongoClient
from search_bar import SearchBar

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


LOCAL = True

es_client = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  {{ resources }}
</head>
<body>
  <div id="myplot"></div>
  <div id="myplot2"></div>
  <script>
  fetch('/plot')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item); })
  </script>
  <script>
  fetch('/plot2')artist = scrap.groupby('artist').size()
artist = artist.sort_values(ascending=True)
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item, "myplot2"); })
  </script>
</body>
""")

client = MongoClient()
db = client["client_name"]
billboard_200 = db["billboard"]





@app.route('/')
def root():
    return page.render(resources=CDN.render())

@app.route('/MusicSearch', methods=('GET', 'POST'))
def MusicSearch():
    form = SearchBar()
    if form.validate_on_submit():
        return redirect('/information/'+form.typing.data)
    return render_template('music_search.html', form=form)

@app.route('/information/<search_word>')
def sucess(search_word):

	df_billboard = pd.DataFrame(list(billboard_200.find()))
	df_billboard_clean = df_billboard.drop(labels='_id',axis='columns')
	documents = df_billboard_clean.fillna("").to_dict(orient="records")
	#bulk(es_client, generate_data(documents))
	
	QUERY = {
	  "query": {
		"multi_match" : {
		  "query":    search_word,
		  "fields": [ "artist", "album" ] 
		}
	  }
	}

	result = es_client.search(index="albums", body=QUERY)
	liste = [elt['_source']['album'] for elt in result["hits"]["hits"]]
	return render_template('results.html',albums=liste)
	
def generate_data(documents):
    for docu in documents:
        yield {
            "_index": "albums",
            "_type": "album",
            "_source": {k:v if v else None for k,v in docu.items()},
        }
        
        
@app.route('/item')
def item():
    output_file("templates/item.html")
    _items = billboard_200.find()
    items = []
    for item in _items:
        items.append(item)
    #items = [item for item in _items]
    #print("collection Eminem: " + str(billboard_200.find_one({"artist":"Eminem"})))
    return render_template('item.html', items=items)

@app.route('/bargraph')
def bargraph():
    output_file("templates/bargraph.html")
    artist = billboard_200.aggregate([{ "$group": { "_id": "$artist", "sum": { "$sum": 1 } } }])
    artist = sorted(list(artist), key=lambda k: k['sum'],reverse=True)
    
    artists = []
    sums = []
    for i in artist:
        artists.append(i["_id"])
        sums.append(i["sum"])

    p = figure(x_range=artists[:20], plot_width=1600,plot_height=800, title="Album Counts", toolbar_location=None, tools="")
    p.vbar(x=artists[:20], top=sums[:20], width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)

    return render_template("bargraph.html")


@app.route('/plot')
def plot():
    scrap = pd.read_json("./newscrawler/newscrawler/spiders/scrap200.json")

    artist = scrap.groupby('artist').size()
    artist = artist.sort_values(ascending=True)

    #p = figure(title = "Iris Morphology", sizing_mode="fixed", plot_width=400, plot_height=400)
    #p.xaxis.axis_label = "artist"
    #p.yaxis.axis_label = "number of albums"
    #p.circle(artist[-20:].index, artist[-20:].values)

    output_file("templates/bar_sorted.html")
    p = figure(x_range=list(artist[-20:].index), plot_width=1600,plot_height=800, title="Album Counts", toolbar_location=None, tools="")
    p.vbar(x=list(artist[-20:].index), top=list(artist[-20:].values), width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    #show(p)
    return render_template("bar_sorted.html")#json.dumps(json_item(p, "myplot"))

@app.route('/test')
def index():
	bar = create_plot()
	return render_template('index.html', plot=bar)


def create_plot():
	scrap = pd.read_json("./newscrawler/newscrawler/spiders/scrap200.json")
	artist = scrap.groupby('artist').size()
	artist = artist.sort_values(ascending=True)
	data = [ go.Bar(x=artist[-20:].index, y = artist[-20:].values)]
	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON #plt.barh(artist[-20:].index, artist[-20:].values, align='center', alpha=0.5)


    #client = MongoClient()
    #print(client.database_names()[1])
	#bb = client["billboard"]

    #Billboard_200 = bb['billboard']

    #return str("collection KIRK: ") + str(Billboard_200.find_one({"album":"KIRK"}))


if __name__ == '__main__':
	print("Running...")
	app.run(debug=True, port=2746)
