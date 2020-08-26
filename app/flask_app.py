from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from app.resources.resources_container import ResourcesContainer

application = Flask(__name__)
resources_container = ResourcesContainer()
configs = resources_container.config()

application.wsgi_app = ProxyFix(application.wsgi_app)
api = Api(application, version=configs['version'], title='BiFrost API', description='Analytic Controller')
CORS(application)