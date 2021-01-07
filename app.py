import os
import signal
from threading import Event
from urllib.parse import urljoin

import psutil
from bson import ObjectId
from flask import Flask, render_template, request, Response
from flask_pymongo import PyMongo

import db
from models import Log, Reading
from worker import TemperatureLogger

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('DATABASE_URL')
app.config["HOST_HOSTNAME"] = os.getenv('HOST_HOSTNAME', os.uname().nodename)
mongo = PyMongo(app)


@app.route('/')
def temperature():
    if (_id := request.args.get('_id', type=ObjectId)) is not None:
        log = mongo.db.temperatures.find_one_or_404({'_id': _id})
        return render_template('content.html', temps=log['temps'])
    else:
        reading = Reading(psutil.sensors_temperatures())
        log = Log(reading)
        mongo.db.temperatures.insert_one(log)
        return render_template('dashboard.html', temps=reading)


def get_abs_url(url):
    """ Returns absolute url by joining post url with base url """
    return urljoin(request.url_root, url)


@app.route('/feeds/temperature_warnings')
def temperature_warnings():
    # search for logs that have a warning flag
    logs = mongo.db.temperatures.find({'warning': True})
    return render_template('temperature.xml', logs=logs, host=app.config['HOST_HOSTNAME'],
                           description="Monitor temperature warnings")


@app.route('/feeds/temperatures/')
def all_temperatures():
    logs = mongo.db.temperatures.find({})
    return Response(render_template('temperature.xml', logs=logs, host=app.config['HOST_HOSTNAME'],
                                    description="Monitor all temperature logs",
                                    updated=mongo.db.temperatures.find_one({})['created']), mimetype="application/xml")


if __name__ == '__main__':
    terminate = Event()

    signal.signal(signal.SIGTERM, terminate.set)

    # initialize database
    db.init_temperatures(mongo)
    # start worker
    worker = TemperatureLogger(mongo, terminate)
    worker.start()
    # start webserver
    app.run(host='0.0.0.0', debug=True)
