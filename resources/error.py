from flask_restful import Resource, reqparse, fields, http_status_message
import logging
import json

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


logging.basicConfig(filename='debug.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


class Error(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']

    def get(self):
        return self.es.search('errors', 'error')['hits']['hits']

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
