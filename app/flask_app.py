from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from app.resources.configurations import Configurations

application = Flask(__name__)
configs = Configurations().configs

application.wsgi_app = ProxyFix(application.wsgi_app)
api = Api(application, version=configs['version'], title=configs['name'], description='Analytic Controller')
CORS(application)

# FlaskInjector(app=application, modules=[configure])

from app.view import notas_view