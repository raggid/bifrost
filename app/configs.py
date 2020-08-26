import json
import os
from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from werkzeug.middleware.proxy_fix import ProxyFix

application = Flask(__name__)

workdir = os.getcwd()

with open(workdir + '/metadata.json') as metadata:
    version = json.load(metadata)['version']

application.wsgi_app = ProxyFix(application.wsgi_app)
api = Api(application, version=version, title='BiFrost API', description='Analytic Controller')
CORS(application)