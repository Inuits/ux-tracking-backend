from flask_restful import Resource, reqparse
from app import jwt_required

post_parser = reqparse.RequestParser()
post_parser.add_argument('id', type=str)
post_parser.add_argument('class', type=str)
post_parser.add_argument('name', type=str)
post_parser.add_argument('value', type=str)
post_parser.add_argument('parent', type=dict)
post_parser.add_argument('type', type=str)
post_parser.add_argument('path', type=str)
post_parser.add_argument('method', type=str)
post_parser.add_argument('timestamp', type=int)

class Action(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']

    @jwt_required
    def get(self):
        return {'hello': True}

    @jwt_required
    def post(self):
        return self.es.index('actions', 'action', post_parser.parse_args())
