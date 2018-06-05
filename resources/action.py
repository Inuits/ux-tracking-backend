from flask import json
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, http_status_message
from rest_framework import status

from resources.ux_resource import UxResource

parser = reqparse.RequestParser()
parser.add_argument('actions', type=str)

filterParser = reqparse.RequestParser()
filterParser.add_argument('client', type=str)
filterParser.add_argument('error_id', type=str)
filterParser.add_argument('id', type=str)
filterParser.add_argument('method', type=str)
filterParser.add_argument('path', type=str)
filterParser.add_argument('position', type=str)
filterParser.add_argument('session', type=str)
filterParser.add_argument('type', type=str)
filterParser.add_argument('value', type=str)


class Action(UxResource):
    def __init__(self, **kwargs):
        super().__init__()
        self.es = kwargs['es']

    @jwt_required
    def get(self):
        for key, value in filterParser.parse_args().items():
            self.esOpts.addFilter(key, value)

        try:
            actions = self.es.search('actions', 'action', self.esOpts.get())

        except:
            actions = []

        return actions('hits') if 'hits' in actions else [], status.HTTP_200_OK

    @jwt_required
    def post(self):
        args = parser.parse_args()
        actions = json.loads(args['actions'])

        for action in actions:
            self.es.index('actions', 'action', action)

        return {}, status.HTTP_201_CREATED
