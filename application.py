from flask import Flask
from os import environ


application = Flask(__name__)


@application.route('/')
def hello_world():
    return 'Hello, World'


@application.route('/testenv')
def testenv():
    envTestEnv = environ.get('TEST_ENV', None)
    return f"Content of TEST_ENV: {envTestEnv}"
