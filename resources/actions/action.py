from flask import json
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, http_status_message

from common.es_options import EsOptions

parser = reqparse.RequestParser()
parser.add_argument('actions', type=str)


class Action(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']
        self.esOpts = EsOptions()

    @jwt_required
    def get(self):
        try:
            actions = self.es.search('actions', 'action', self.esOpts.get())

        except:
            actions = []

        return actions['hits'] if 'hits' in actions else []

    @jwt_required
    def post(self):
        args = parser.parse_args()
        actions = json.loads(args['actions'])

        for action in actions:
            self.es.index('actions', 'action', action)

        return http_status_message(200)
