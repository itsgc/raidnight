from flask import Flask


application = Flask(__name__)


@application.route('/')
def hello_world():
    return 'Hello, World'


@application.route('/testenv')
def testenv():
    return f"Content of TEST_ENV: {environ['TEST_ENV']}"
