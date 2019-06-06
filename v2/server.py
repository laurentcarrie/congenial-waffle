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

if __name__ == '__main__':
    client = MongoClient(cnx.URI);
    db = client.test1
    # sample = db.find_one({'listing_url': 'https://www.airbnb.com/rooms/10006546'})
    # print(sample)
    logger.info("Connection to {0} Successful".format(cnx.URI))
    app.db = db
    app.run()
