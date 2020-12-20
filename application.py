from flask import Flask
from flask import jsonify
from os import environ


application = Flask(__name__)


@application.route('/')
def hello_world():
    return 'Hello, World'


@application.route('/testenv')
def testenv():
    envTestEnv = environ.get('TEST_ENV', None)
    return f"Content of TEST_ENV: {envTestEnv}"


@application.route('/testjson')
def testjson():
    sampledata = list()
    samplemember = {"ilvl": 195,
                    "name": "karmik",
                    "realm": "sunstrider",
                    "spec": "guardian",
                    "role": "raider"}
    sampledata.append(samplemember)
    samplemember2 = {"ilvl": 151,
                     "name": "ylima",
                     "realm": "sunstrider",
                     "spec": "protection",
                     "role": "initiate"}
    sampledata.append(samplemember2)
    return jsonify(sampledata)
