from pymongo import MongoClient
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    #client = MongoClient("mongo")
    #bb = client["client_name"]

    #Billboard_200 = bb['billboard']
    #return str("collection KIRK: ") + str(Billboard_200.find_one({"album":"KIRK"}))
    return 'aa'

if __name__ == '__main__':
    app.run(debug=True, port=2745)
