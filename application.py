from blizzard import BlizzardTools
from flask import Flask
from flask import jsonify
from flask_basicauth import BasicAuth
from os import environ


application = Flask(__name__)

application.config['BASIC_AUTH_USERNAME'] = environ['BASIC_AUTH_USERNAME']
application.config['BASIC_AUTH_PASSWORD'] = environ['BASIC_AUTH_PASSWORD']

basic_auth = BasicAuth(application)

auth_data = {"client_id": environ.get("CLIENT_ID"),
             "client_secret": environ.get("CLIENT_SECRET")}

blizzardtools = BlizzardTools(auth_data)


@application.route('/')
def hello_world():
    return 'Hello, World'


@application.route('/testenv')
def testenv():
    envTestEnv = environ.get('TEST_ENV', None)
    return f"Content of TEST_ENV: {envTestEnv}"


@application.route('/testjson/<realm>/<guild>')
@basic_auth.required
def testjson(realm, guild):
    response = blizzardtools.get_raiders(realm, guild)
    return jsonify(response)
