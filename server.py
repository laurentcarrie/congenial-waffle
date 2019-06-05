from flask import Flask, render_template, request, stream_with_context
import json

from flask_marshmallow import Marshmallow

from flask import Response

import datetime
from pymongo import MongoClient

import cnx

from model import Car


app = Flask(__name__)

ma = Marshmallow(app)

added_cols = 20



@app.route('/')
def display():
    return "Looks like it works!"


names = ['pomme', 'poire', 'orange']



@app.route('/demo')
def demo():
    t1 = datetime.datetime.now()
    cars = app.db.find(limit=100000000)
    cars = [ Car(c) for c in cars]
    added_cols=20
    page = render_template('demo.html', added_cols=added_cols, names=names, cars=cars,
                    addCols=range(added_cols))
    t2 = datetime.datetime.now()
    print("time : ",t2-t1)
    return Response(page)

@app.route('/demo2',methods=['GET'])
def demo2():
    limit = request.args.get('limit')
    addded_cols=20
    page = render_template('demo2.html', limit=limit,added_cols=range(added_cols))
    return page



@app.route('/data',methods=['GET'])
def return_data():
    limit = request.args.get('limit')
    limit=int(limit)
    sample = app.db.find(limit=limit)

    #data = json.dumps(data)
    #return flask.Response(flask.stream_with_context(generate()))
    def generate():
        yield '['
        not_first=False
        for s in sample:
            if not_first:
                yield ','
            not_first = True
            yield json.dumps(Car(s).to_dict())
        yield ']'
    return Response(generate(),mimetype="text/json")

if __name__ == '__main__':
    client = MongoClient(cnx.URI);
    db = client.test1.cars
    #sample = db.find_one({'listing_url': 'https://www.airbnb.com/rooms/10006546'})
    #print(sample)
    print("Connection Successful")
    app.db = db
    app.run()
