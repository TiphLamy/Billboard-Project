# flask env: ./flask_env/bin/activate

from flask import Flask
from flask import request
from flask import render_template, render_template_string
from flask import Flask, flash, redirect, render_template, \
     request, url_for
#from flask_pymongo import PyMongo
from pymongo import MongoClient
from search_bar import SearchBar

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import pandas as pd
import numpy as np

LOCAL = True

es_client = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
#app.config['MONGO_URL'] = '27017'
#mongo = PyMongo(app,uri='mongodb://localhost:27017')

client = MongoClient()
db = client["client_name"]
billboard = db["billboard"]

df_billboard = pd.DataFrame(list(billboard.find()))
df_billboard_clean = df_billboard.drop(labels='_id',axis='columns')
documents = df_billboard_clean.fillna("").to_dict(orient="records")

def generate_data(documents):
    for docu in documents:
        yield {
            "_index": "albums",
            "_type": "album",
            "_source": {k:v if v else None for k,v in docu.items()},
        }


@app.route('/')
def rien():
	
	return redirect('/MusicSearch')


@app.route('/MusicSearch', methods=('GET', 'POST'))
def MusicSearch():
    form = SearchBar()
    if form.validate_on_submit():
        return redirect('/information/'+form.typing.data)
    return render_template('music_search.html', form=form)


@app.route('/information/<search_word>')
def sucess(search_word):

	
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
	result = es_client.search(index="albums", body=QUERY)
	album = [elt['_source']['album'] for elt in result["hits"]["hits"]]
	artist = [elt['_source']['artist'] for elt in result["hits"]["hits"]]
	rank = [elt['_source']['rank'] for elt in result["hits"]["hits"]]
	return render_template('results.html',albums=album,artists=artist,ranks=rank)



if __name__ == '__main__':
    app.run(debug=True, port=2745) 
