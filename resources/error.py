import json

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, fields, http_status_message

from common.es_options import EsOptions

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


class Error(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']

    @jwt_required
    def get(self):

        esOpts = EsOptions()

        try:
            errors = self.es.search('errors', 'error', esOpts.get())

        except:
            errors = []

        return errors['hits'] if 'hits' in errors else []

    @jwt_required
    def post(self):
        args = post_parser.parse_args()
        actions = json.loads(args['actions'])

        del args['actions']

        error = self.es.index('errors', 'error', args)

        for action in actions:
            action['error_id'] = error['_id']
            self.es.index('actions', 'action', action)

        return http_status_message(200)
