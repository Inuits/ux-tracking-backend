import logging

from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager, jwt_required
from flask_restful import Api
from flask_restful.utils import cors

from resources.action import Action
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
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.decorators=[cors.crossdomain(origin='*')]
es = Elasticsearch()

# JWT
app.config['JWT_SECRET_KEY'] = 'SUPERsecretAPPkeyFORjqueryLOGGER*'
jwt = JWTManager(app)

# creating ES index for actions with parent (error)
if not es.indices.exists('actions'):
    es.indices.create('actions')

    es.indices.put_mapping(
        index='actions', doc_type='action', body={
            '_parent': {
                'type': 'errors'
            }
        }
    )

# create the routes
api.add_resource(Auth, '/auth')
api.add_resource(Error, '/error', resource_class_kwargs={'es': es})
api.add_resource(Action, '/action', resource_class_kwargs={'es': es})

# register blueprint
app.register_blueprint(api_bp)
