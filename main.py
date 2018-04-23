from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from elasticsearch import Elasticsearch

app = Flask(__name__)
api = Api(app)
es = Elasticsearch()


class Test(Resource):
    def get(self):
        return es.search('users')['hits']['hits']

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username is required")
        parser.add_argument('name', required=True, help="Name is required")

        args = parser.parse_args()
        es.create('users', 'user', 0, {'name': args['name'], 'username': args['username']})


api.add_resource(Test, '/')
