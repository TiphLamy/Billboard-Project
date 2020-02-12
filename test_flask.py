from pymongo import MongoClient
from flask import Flask
import pandas as pd
import json
app = Flask(__name__)

@app.route('/test')
def hello_world():
	scrap = pd.read_json("./newscrawler/newscrawler/spiders/scrap200.json")
    	#client = MongoClient()
    	#print(client.database_names()[1])
		#bb = client["billboard"]

    	#Billboard_200 = bb['billboard']
    return scrap
    #return str("collection KIRK: ") + str(Billboard_200.find_one({"album":"KIRK"}))


if __name__ == '__main__':
    print("Running...")
    app.run(debug=True, port=2746)
