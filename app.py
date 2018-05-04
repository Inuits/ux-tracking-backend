from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restful import Api

from resources.action import Action
from resources.error import Error

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
es = Elasticsearch()

if not es.indices.exists('actions'):
    es.indices.create('actions')

    es.indices.put_mapping(
        index='actions', doc_type='action', body={
            '_parent': {
                'type': 'errors'
            }
        }
    )

api.add_resource(Error, '/error', resource_class_kwargs={'es': es})
api.add_resource(Action, '/action', resource_class_kwargs={'es': es})

app.register_blueprint(api_bp)
CORS(app, resources={r"/*": {"origins": "*"}})
