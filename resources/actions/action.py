from flask import json
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, http_status_message

parser = reqparse.RequestParser()
parser.add_argument('actions', type=str)


class Action(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']

    @jwt_required
    def get(self):
        try:
            actions = self.es.search('actions', 'action', {
                'sort': {
                    'timestamp': {'order': 'desc'}
                },
                'size': 100
            })

        except:
            actions = []

        return actions['hits']['hits'] if 'hits' in actions else []

    @jwt_required
    def post(self):
        args = parser.parse_args()
        actions = json.loads(args['actions'])

        for action in actions:
            self.es.index('actions', 'action', action)

        return http_status_message(200)
