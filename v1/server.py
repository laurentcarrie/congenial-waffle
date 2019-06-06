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
    return "Looks like it works!"


names = ['pomme', 'poire', 'orange']


@app.route('/demo')
def demo():
    t1 = datetime.datetime.now()
    cars = app.db.cars.find(filter={"price": "{$lt:10000.7}"}, limit=100000000)
    cars = [Car(c) for c in cars]
    added_cols = 20
    page = render_template('demo.html', added_cols=added_cols, names=names, cars=cars,
                           addCols=range(added_cols))
    t2 = datetime.datetime.now()
    print("time : ", t2 - t1)
    return Response(page)


@app.route('/demo2', methods=['GET'])
def demo2():
    limit = request.args.get('limit')
    addded_cols = 20
    page = render_template('demo2.html', limit=limit, added_cols=range(added_cols))
    return page

@app.route('/demo3', methods=['GET'])
def demo3():
    page = render_template('demo3.html')
    return page


@app.route('/make_data3')
def make_data3():
    mapper = Code(""" function() {
        var key = { model:this.model , make:this.make } ;
       var value = this.price ;
       emit(key, this.price) ;
    }
    """)

    reducer = Code("""     function (key, values) {
        var reducedObject = {
          model: key,
           total_price: 0,
       };

       var sum=0 ;
       for (var index=0;index<values.length;++index) {
           sum += values[index]
       }

        return sum ;
    };
    """)

    result = app.db.cars.map_reduce(mapper, reducer, "myresults")
    return "done"

@app.route('/data', methods=['GET'])
def return_data():
    limit = request.args.get('limit')
    limit = int(limit)
    # sample = app.db.find({"price": {"$lt": 10000.1}},limit=limit)
    sample = app.db.cars.find(limit=limit)

    # data = json.dumps(data)
    # return flask.Response(flask.stream_with_context(generate()))
    def generate():
        yield '['
        not_first = False
        for s in sample:
            if not_first:
                yield ','
            not_first = True
            yield json.dumps(Car(s).to_dict())
        yield ']'

    return Response(generate(), mimetype="text/json")

@app.route('/data3', methods=['GET'])
def return_data3():
    make_data3()
    sample = app.db.myresults.find()

    # data = json.dumps(data)
    # return flask.Response(flask.stream_with_context(generate()))
    def generate():
        yield '['
        not_first = False
        for s in sample:
            if not_first:
                yield ','
            not_first = True
            d = { 'model' : s['_id']['model'],'make':s['_id']['make'],'price':s['value']}
            logger.info(d)
            yield(json.dumps(d))
        yield ']'

    return Response(generate(), mimetype="text/json")

if __name__ == '__main__':
    client = MongoClient(cnx.URI);
    db = client.test1
    # sample = db.find_one({'listing_url': 'https://www.airbnb.com/rooms/10006546'})
    # print(sample)
    logger.info("Connection to {0} Successful".format(cnx.URI))
    app.db = db
    app.run()
