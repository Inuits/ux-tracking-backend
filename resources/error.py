from flask_restful import Resource, reqparse, fields, marshal_with
from resources.action import Action

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
post_parser.add_argument('actions')


class Error(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']

    def get(self):
        return self.es.search('errors', 'error')['hits']['hits']

    def post(self):
        args = post_parser.parse_args()

        actions = args['actions']
        del args['actions']

        error = self.es.index('errors', 'error', args)


        results = []
        # doc_type = {'_parent': {'type': 'errors', 'id': error['_id']}}
        doc_type = {'_parent': {'id': error['_id']}}
        for action in actions:
            action['doc_type'] = doc_type
            results.append(
                self.es.index('actions', 'action', action)

                # Action(es=self.es).post()
            )

        return results
