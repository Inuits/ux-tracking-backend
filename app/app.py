from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

# app initializion
from app.resources.actions import Actions
from app.resources.auth import Auth
from app.resources.errors import Errors

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True, automatic_options=True,
     expose_headers=['Authorization'])

app.config['CORS_HEADERS'] = 'Content-Type'
api_bp = Blueprint('api', __name__)

api = Api(api_bp)
es = Elasticsearch()

es.indices.create('errors', ignore=400, body={
    "analysis": {
        "analyzer": {
            "default": {
                "tokenizer": "whitespace",
                "filter": ["lowercase"]
            }
        }
    }
})
es.indices.create('actions', ignore=400, body={
    "analysis": {
        "analyzer": {
            "default": {
                "tokenizer": "whitespace",
                "filter": ["lowercase"]
            }
        }
    }
})

# JWT
app.config['JWT_SECRET_KEY'] = 'SUPERsecretAPPkeyFORjqueryLOGGER*'
jwt = JWTManager(app)

# create the routes
api.add_resource(Auth, '/auth')
api.add_resource(Errors, '/error', '/error/<error_id>', resource_class_kwargs={'es': es})
api.add_resource(Actions, '/action', resource_class_kwargs={'es': es})

# register blueprint
app.register_blueprint(api_bp)
