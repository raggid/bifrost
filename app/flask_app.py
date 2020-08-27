from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from app.container import Container

application = Flask(__name__)
configs = Container.configs()

application.wsgi_app = ProxyFix(application.wsgi_app)
api = Api(application, version=configs['version'], title='BiFrost API', description='Analytic Controller')
CORS(application)

from app.view import notas_view