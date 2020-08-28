from envyaml import EnvYAML
from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from werkzeug.middleware.proxy_fix import ProxyFix

application = Flask(__name__)

configs = EnvYAML('metadata.yaml')

application.wsgi_app = ProxyFix(application.wsgi_app)
api = Api(application, version=configs['version'], title=configs['name'], description='Analytic Controller')
CORS(application)