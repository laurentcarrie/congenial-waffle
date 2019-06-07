from flask import Flask, render_template, request
import json
from flask import Response
import logging

import datetime
from pymongo import MongoClient
from bson.code import Code

from v1 import cnx

from v1.model import Car

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

app = Flask(__name__)

added_cols = 20


@app.route('/')
def display():
    page = render_template('index.html')
    return page

def getRows_1():
    # level 1
{
  "startRow": 0,
  "endRow": 1000,
  "rowGroupCols": [
    {
      "id": "make",
      "displayName": "make",
      "field": "make"
    }
  ],
  "valueCols": [
    {
      "id": "price",
      "aggFunc": "sum",
      "displayName": "price",
      "field": "price"
    }
  ],
  "pivotCols": [],
  "pivotMode": false,
  "groupKeys": [],
  "filterModel": {},
  "sortModel": []
}

def dispatch(requete):
    if (len(requete["rowGroupCols"]) == 1 and requete["rowGroupCols"][0]["id"]=="make" and len(requete["valueCols"])==1
        and requete["valueCols"][0]["id"]=="price"
        and requete["pivotCols"]==[]
        and requete["pivotMode"]==False
        and requete["filterModel"]==[]
        and requete["sortModel"]==[]) :
        return getRows_1(requete)
    raise Exception('request not managed')


def getRows_2(j):


@app.route('/getRows', methods=['POST'])
def getRows():
    j = request.get_json()
    method = dispatch(j)
    return method()

    startRow = j['startRow']
    endRow = j['endRow']
    logger.info("get row from {0} to {1}".format(startRow,endRow))

    rowGroupId = j['rowGroupCols'][0]['id']
    logger.info("group on {0}".format(rowGroupId))
    #db.getCollection('cars').aggregate([{$group: {_id: "$make", total: {$sum: "$price"}}}])
    # sample = app.db.find({"price": {"$lt": 10000.1}},limit=limit)
    sample = app.db.cars.find(limit=endRow-startRow).skip(startRow)

    # data = json.dumps(data)
    # return flask.Response(flask.stream_with_context(generate()))
    def generate():
        yield '{ "data":'
        yield '['
        not_first = False
        for s in sample:
            if not_first:
                yield ','
            not_first = True
            yield json.dumps(Car(s).to_dict())
        yield ']'
        yield '}'

    return Response(generate(), mimetype="text/json")


if __name__ == '__main__':
    client = MongoClient(cnx.URI);
    db = client.test1
    # sample = db.find_one({'listing_url': 'https://www.airbnb.com/rooms/10006546'})
    # print(sample)
    logger.info("Connection to {0} Successful".format(cnx.URI))
    app.db = db
    app.run()
