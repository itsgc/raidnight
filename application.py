from blizzard import BlizzardTools
from flask import Flask
from flask import jsonify
from flask import request
from flask_basicauth import BasicAuth
from requests.exceptions import HTTPError
from os import environ
from logging.config import dictConfig


logging_level = environ['LOG_LEVEL']

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': 'timestamp=%(asctime)s,level=%(levelname)s,message="%(message)s"',
        'datefmt': '%Y-%m-%dT%H:%M:%S'
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': logging_level,
        'handlers': ['wsgi']
    }
})

application = Flask(__name__)

application.config['BASIC_AUTH_USERNAME'] = environ['BASIC_AUTH_USERNAME']
application.config['BASIC_AUTH_PASSWORD'] = environ['BASIC_AUTH_PASSWORD']

basic_auth = BasicAuth(application)

auth_data = {"client_id": environ.get("CLIENT_ID"),
             "client_secret": environ.get("CLIENT_SECRET")}

blizzardtools = BlizzardTools(auth_data)

# raise GenericAPIError(message=e.message, status_code=500)

# Custom Exceptions to return contextual HTTP error codes.


class GenericAPIError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class ResourceNotFound(Exception):
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class RequestFailed(Exception):
    status_code = 503

    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class UnauthorizedRequest(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@application.route('/')
def go_away():
    application.logger.info(f'{request.remote_addr} requested {request.url}')
    response = {"status": "OK",
                "message": "Nothing to see here"}
    return jsonify(response)


@application.route('/rostermanager/<realm>/<guild>')
@basic_auth.required
def rostermanager(realm, guild):
    application.logger.info(f'{request.remote_addr} requested {request.url}')
    try:
        response = blizzardtools.get_raiders(realm, guild)
        application.logger.info(f'fetched guild member data for {guild}_{realm},{len(response)} records found')
        return jsonify(response)
    except HTTPError as e:
        application.logger.error(f'failed fetching upstream data, {e}')

        raise GenericAPIError('Failed fetching upstream data')


@application.errorhandler(GenericAPIError)
def handle_generic_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@application.errorhandler(ResourceNotFound)
def handle_resource_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@application.errorhandler(RequestFailed)
def handle_request_failed(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@application.errorhandler(UnauthorizedRequest)
def handle_unauthorized_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
