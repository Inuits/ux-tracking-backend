import json

from flask_restful import Resource, reqparse, fields, http_status_message

from app import jwt_required

error_fields = {
    'error': fields.String,
    'source': fields.String,
    'position': fields.String,
    'stack': fields.String,
    'actions': fields.List,
}

post_parser = reqparse.RequestParser()
post_parser.add_argument('error', type=str)
post_parser.add_argument('source', type=str)
post_parser.add_argument('position', type=str)
post_parser.add_argument('stack', type=str)
post_parser.add_argument('actions', type=str)


class Error(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']

    @jwt_required
    def get(self):
        return self.es.search('errors', 'error')['hits']['hits']

    @jwt_required
    def post(self):
        args = post_parser.parse_args()
        actions = json.loads(args['actions'])

        del args['actions']

        error = self.es.index('errors', 'error', args)

        results = []
        for action in actions:
            results.append(
                self.es.index('actions', 'action', action, parent=error['_id'])
            )

        return http_status_message(200)
