import yaml
from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.resources.actions import Actions
from app.resources.auth import Auth
from app.resources.errors import Errors


def getConfig():
    config = {}
    with open('config/config.yml') as f:
        config = yaml.load(f)

    return config


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True, automatic_options=True,
     expose_headers=['Authorization'])

app.config['CORS_HEADERS'] = 'Content-Type'
api_bp = Blueprint('api', __name__)

config = getConfig()

api = Api(api_bp)
es = Elasticsearch(
    [config['elasticsearch']['host']],
    port=config['elasticsearch']['port']
)

# ES Indeces
body = {
    "analysis": {
        "analyzer": {
            "default": {
                "tokenizer": "whitespace",
                "filter": ["lowercase"]
            }
        }
    }
}
es.indices.create('errors', ignore=400, body=body)
es.indices.create('actions', ignore=400, body=body)

# JWT
app.config['JWT_SECRET_KEY'] = config['jwt_secret_key']
jwt = JWTManager(app)

# create the routes
api.add_resource(Auth, '/auth', resource_class_kwargs={'apps': config['keys']})
api.add_resource(Errors, '/error', '/error/<error_id>', resource_class_kwargs={'es': es})
api.add_resource(Actions, '/action', resource_class_kwargs={'es': es})

# register blueprint
app.register_blueprint(api_bp)
