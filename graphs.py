from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import json
import numpy as np
from bokeh.embed import json_item
from bokeh.resources import CDN
from jinja2 import Template
from bokeh.io import show, output_file
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
import os
from pymongo import MongoClient

from flask import render_template, render_template_string
app = Flask(__name__)


client = MongoClient()
db = client["client_name"]
billboard_200 = db["billboard"]



def create_bargraph():
    output_file("templates/music_search.html")
    _items = billboard_200.find()
    items = []
    for item in _items:
        items.append(item)

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
    plot = create_bar_chart(data, "Album Counts", "artist", "sum", hover)
    script, div = components(plot)

    return render_template('music_search.html', items=artist, the_div=div, the_script=script)

def create_hover_tool():
    """Generates the HTML for the Bokeh's hover data tool on our graph."""
    """Generates the HTML for the Bokeh's hover data tool on our graph."""
    # hover_html = """
    #   <div>
    #     <span class="hover-tooltip">$x</span>
    #   </div>
    #   <div>
    #     <span class="hover-tooltip">@sums count</span>
    #   </div>
    # """
    # return HoverTool(tooltips=hover_html)
    return None

def create_bar_chart(data, title, x_name, y_name, hover_tool=None, width=1200, height=300):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
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
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Number of albums in the top 200"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.major_label_orientation = 1
    return plot



if __name__ == '__main__':
  print("Running...")
  app.run(debug=True, port=2746)
