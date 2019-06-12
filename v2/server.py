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
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

app = Flask(__name__)

added_cols = 20


def getRows_1(j):
    logger.info("dispatch 1")
    startRow = j['startRow']
    endRow = j['endRow']
    logger.info("get row from {0} to {1}".format(startRow, endRow))

    # db.getCollection('cars').aggregate([{$group: {_id: "$make", total: {$sum: "$price"}}}])
    # sample = app.db.find({"price": {"$lt": 10000.1}},limit=limit)
    # sample = app.db.cars.find(limit=endRow-startRow).skip(startRow)
    sample = app.db.cars.aggregate([{"$group": {"_id": "$make", "price": {"$sum": "$price"}}}])

    # data = json.dumps(data)
    # return flask.Response(flask.stream_with_context(generate()))
    def generate():
        count = 0
        yield '{ "data":'
        yield '['
        not_first = False
        for s in sample:
            if not_first:
                yield ','
            not_first = True
            d = {"make": s["_id"], "price": s["price"]}
            yield json.dumps(d)
            count = count + 1
        yield ']'
        yield ',"lastRow":' + str(count + startRow)
        yield '}'

    def ret():
        return Response(generate(), mimetype="text/json")

    return ret


def getRows_2(j):
    logger.info("dispatch 2")
    startRow = j['startRow']
    endRow = j['endRow']
    groupKeys = j['groupKeys'][0]
    logger.info("get row from {0} to {1}".format(startRow, endRow))

    # db.getCollection('cars').aggregate([{$group: {_id: "$make", total: {$sum: "$price"}}}])
    # sample = app.db.find({"price": {"$lt": 10000.1}},limit=limit)
    # sample = app.db.cars.find(limit=endRow-startRow).skip(startRow)
    sample = app.db.cars.find({"make": groupKeys}).skip(startRow).limit(endRow - startRow)

    # data = json.dumps(data)
    # return flask.Response(flask.stream_with_context(generate()))
    def generate():
        count = 0
        yield '{ "data":'
        yield '['
        not_first = False
        for s in sample:
            if not_first:
                yield ','
            not_first = True
            d = {"make": s["make"], "model": s["model"], "price": s["price"], "index": s["index"]}
            yield json.dumps(d)
            count = count + 1
        yield ']'
        #        yield ',"lastRow":' + str(count+startRow)
        yield '}'

    def ret():
        return Response(generate(), mimetype="text/json")

    return ret


def getRows_4(j):
    logger.info("dispatch 4")
    startRow = j['startRow']
    endRow = j['endRow']
    logger.info("get row from {0} to {1}".format(startRow, endRow))

    # db.getCollection('cars').aggregate([{$group: {_id: "$make", total: {$sum: "$price"}}}])
    # sample = app.db.find({"price": {"$lt": 10000.1}},limit=limit)
    # sample = app.db.cars.find(limit=endRow-startRow).skip(startRow)
    sample_1 = db.cars.aggregate([
        {"$group": {"_id": "$make", "price": {"$sum": "$price"}}},
    ])
    sample = db.cars.aggregate([
        {"$group": {"_id": {"make": "$make", "model": "$model"}, "price": {"$sum": "$price"}}},
    ])

    # data = json.dumps(data)
    # return flask.Response(flask.stream_with_context(generate()))
    def generate():
        count = 0
        yield '{ "data":'
        yield '['
        not_first = False
        for s in sample_1:
            logger.info(s)
            if not_first:
                yield ','
            not_first = True
            d = {"make": s["_id"], "price": s["price"]}
            #d = {"make": s["_id"]["make"], "model": s["_id"]["model"], "price": s["price"]}
            yield json.dumps(d)
            count = count + 1
        yield ']'
        if count < endRow - startRow:
                yield ',"lastRow":' + str(count+startRow)
        yield '}'

    def ret():
        return Response(generate(), mimetype="text/json")

    return ret


#db.getCollection('cars').aggregate([
 #   {$group: {"_id":{make:"$make",model:"$model"},price:{$sum:"$price"}}},
 #   {$project:{_id:false,make:"$_id.make",model:"$_id.model",price:true}},

    ])
def getRows_5(j):
    logger.info("dispatch 5")
    startRow = j['startRow']
    endRow = j['endRow']
    groupKeys = j["groupKeys"]
    logger.info("get row from {0} to {1}".format(startRow, endRow))

    # db.getCollection('cars').aggregate([{$group: {_id: "$make", total: {$sum: "$price"}}}])
    # sample = app.db.find({"price": {"$lt": 10000.1}},limit=limit)
    # sample = app.db.cars.find(limit=endRow-startRow).skip(startRow)

    sample = db.cars.aggregate([
        {"$group": {"_id": { "make":"$make","model":"$model"},"price": {"$sum": "$price"}}},
        {"$match":{"make":"Toyota"}}
    ])

    # data = json.dumps(data)
    # return flask.Response(flask.stream_with_context(generate()))
    def generate():
        count = 0
        yield '{ "data":'
        yield '['
        not_first = False
        for s in sample:
            display(s)
            if not_first:
                yield ','
            not_first = True
            d = {"make": s["_id"]["make"], "model": s["_id"]["model"], "price": s["price"]}
            yield json.dumps(d)
            count = count + 1
        yield ']'
        #        yield ',"lastRow":' + str(count+startRow)
        yield '}'

    def ret():
        return Response(generate(), mimetype="text/json")

    return ret

def getRows_3(j):
    logger.info("dispatch 3")
    startRow = j['startRow']
    endRow = j['endRow']
    logger.info("get row from {0} to {1}".format(startRow, endRow))

    # db.getCollection('cars').aggregate([{$group: {_id: "$make", total: {$sum: "$price"}}}])
    # sample = app.db.find({"price": {"$lt": 10000.1}},limit=limit)
    # sample = app.db.cars.find(limit=endRow-startRow).skip(startRow)
    sample = app.db.cars.find().skip(startRow).limit(endRow - startRow)

    # data = json.dumps(data)
    # return flask.Response(flask.stream_with_context(generate()))
    def generate():
        count = 0
        yield '{ "data":'
        yield '['
        not_first = False
        for s in sample:
            if not_first:
                yield ','
            not_first = True
            d = {"make": s["make"], "model": s["model"], "price": s["price"], "index": s["index"]}
            yield json.dumps(d)
            count = count + 1
        yield ']'
        #        yield ',"lastRow":' + str(count+startRow)
        yield '}'

    def ret():
        return Response(generate(), mimetype="text/json")

    return ret


def dispatch(requete):
    if (
            len(requete["groupKeys"]) == 0 and
            len(requete["rowGroupCols"]) == 1
            and requete["rowGroupCols"][0]["id"] == "make"
            and len(requete["valueCols"]) == 1
            and requete["valueCols"][0]["id"] == "price"
            and requete["pivotCols"] == []
            and requete["pivotMode"] == False
            and requete["filterModel"] == {}
            and requete["sortModel"] == []
    ):
        return getRows_1(requete)

    elif (
            len(requete["groupKeys"]) == 1
            and len(requete["rowGroupCols"]) == 1
            and requete["rowGroupCols"][0]["id"] == "make"
            and len(requete["valueCols"]) == 1
            and requete["valueCols"][0]["id"] == "price"
            and requete["pivotCols"] == []
            and requete["pivotMode"] == False
            and requete["filterModel"] == {}
            and requete["sortModel"] == []
    ):
        return getRows_2(requete)

    elif (
            len(requete["rowGroupCols"]) == 2
            and requete["rowGroupCols"][0]["id"] == "make"
            and requete["rowGroupCols"][0]["id"] == "make"
            and requete.get("groupKeys") == []
            and len(requete["valueCols"]) == 1
            and requete["valueCols"][0]["id"] == "price"
            and requete["pivotCols"] == []
            and requete["pivotMode"] == False
            and requete["filterModel"] == {}
            and requete["sortModel"] == []
    ):
        return getRows_4(requete)

    elif (
            len(requete["groupKeys"]) == 1
            and len(requete["rowGroupCols"]) == 2
            and requete["rowGroupCols"][0]["id"] == "make"
            and requete["rowGroupCols"][1]["id"] == "model"
            and len(requete["valueCols"]) == 1
            and requete["valueCols"][0]["id"] == "price"
            and requete["pivotCols"] == []
            and requete["pivotMode"] == False
            and requete["filterModel"] == {}
            and requete["sortModel"] == []
    ):
        return getRows_5(requete)


    elif (
            len(requete["groupKeys"]) == 0
            and len(requete["rowGroupCols"]) == 0
            and len(requete["valueCols"]) == 1
            and requete["valueCols"][0]["id"] == "price"
            and requete["pivotCols"] == []
            and requete["pivotMode"] == False
            and requete["filterModel"] == {}
            and requete["sortModel"] == []
    ):
        return getRows_3(requete)

    logger.error(requete)
    raise Exception('request not managed')


@app.route('/')
def display():
    page = render_template('index.html')
    return page


@app.route('/getRows', methods=['POST'])
def getRows():
    j = request.get_json()
    logger.info(j)
    method = dispatch(j)
    return method()


if __name__ == '__main__':
    client = MongoClient(cnx.URI);
    db = client.test1
    # sample = db.find_one({'listing_url': 'https://www.airbnb.com/rooms/10006546'})
    # print(sample)
    logger.info("Connection to {0} Successful".format(cnx.URI))
    app.db = db
    app.run()
