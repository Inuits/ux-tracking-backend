import json

from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields, http_status_message
from rest_framework import status

from resources.ux_resource import UxResource

error_fields = {
    'error': fields.String,
    'source': fields.String,
    'position': fields.String,
    'stack': fields.String,
    'actions': fields.List,
}

post_parser = reqparse.RequestParser()
post_parser.add_argument('client', type=str)
post_parser.add_argument('session', type=str)
post_parser.add_argument('error', type=str)
post_parser.add_argument('source', type=str)
post_parser.add_argument('position', type=str)
post_parser.add_argument('stack', type=str)
post_parser.add_argument('actions', type=str)
post_parser.add_argument('timestamp', type=int)


class Error(UxResource):
    def __init__(self, **kwargs):
        super().__init__()
        self.es = kwargs['es']

    @jwt_required
    def get(self):
        statusCode = status.HTTP_200_OK

        try:
            errors = self.es.search('errors', 'error', self.esOpts.get())

        except:
            errors = []
            statusCode = status.HTTP_204_NO_CONTENT

        return errors['hits'] if 'hits' in errors else [], statusCode

    @jwt_required
    def post(self):
        args = post_parser.parse_args()
        actions = json.loads(args['actions'])

        del args['actions']

        error = self.es.index('errors', 'error', args)

        for action in actions:
            action['error_id'] = error['_id']
            self.es.index('actions', 'action', action)

        return {}, status.HTTP_201_CREATED
