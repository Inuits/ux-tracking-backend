import logging

from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.actions.action import Action
from resources.actions.actions_for_error import ActionsForError
from resources.auth import Auth
from resources.error import Error

# Logging TODO remove
logging.basicConfig(filename='debug.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

# app initializion
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True, automatic_options=True,
     expose_headers=['Authorization'])
app.config['CORS_HEADERS'] = 'Content-Type'
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
es = Elasticsearch()

if not es.indices.exists('errors'):
    es.indices.create('errors')

if not es.indices.exists('actions'):
    es.indices.create('actions')

# JWT
app.config['JWT_SECRET_KEY'] = 'SUPERsecretAPPkeyFORjqueryLOGGER*'
jwt = JWTManager(app)

# create the routes
api.add_resource(Auth, '/auth')
api.add_resource(Error, '/error', resource_class_kwargs={'es': es})
api.add_resource(Action, '/action', resource_class_kwargs={'es': es})
api.add_resource(ActionsForError, '/action/for/<string:error_id>', resource_class_kwargs={'es': es})

# register blueprint
app.register_blueprint(api_bp)
