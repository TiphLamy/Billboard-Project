from pymongo import MongoClient
from flask import Flask
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

from flask import render_template, render_template_string
app = Flask(__name__)

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


@app.route('/')
def root():
    return page.render(resources=CDN.render())

@app.route('/plot')
def plot():
    scrap = pd.read_json("./newscrawler/newscrawler/spiders/scrap200.json")
    artist = scrap.groupby('artist').size()
    artist = artist.sort_values(ascending=True)

    #p = figure(title = "Iris Morphology", sizing_mode="fixed", plot_width=400, plot_height=400)
    #p.xaxis.axis_label = "artist"
    #p.yaxis.axis_label = "number of albums"
    #p.circle(artist[-20:].index, artist[-20:].values)

    output_file("bar_sorted.html")
    p = figure(x_range=list(artist[-20:].index), plot_height=350, title="Album Counts", toolbar_location=None, tools="")
    p.vbar(x=list(artist[-20:].index), top=list(artist[-20:].values), width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)
    return redirect_to_url("bar_sorted.html")#json.dumps(json_item(p, "myplot"))

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
