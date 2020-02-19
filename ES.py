from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import pandas as pd
import json
import numpy as np

LOCAL = False
es_client = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])

df_billboard = pd.read_json("./newscrawler/newscrawler/spiders/scrap200.json")
documents = df_billboard.fillna("").to_dict(orient="records")

def generate_data(documents):
    for docu in documents:
        yield {
            "_index": "albums",
            "_type": "album",
            "_source": {k:v if v else None for k,v in docu.items()},
        }

bulk(es_client, generate_data(documents))

QUERY = {
  "query": {
    "multi_match" : {
      "query":    "Malone",
      "fields": [ "artist" ] 
    }
  }
}
result = es_client.search(index="albums", body=QUERY)
[elt['_source']['album'] for elt in result["hits"]["hits"]]
