from flask import json
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, http_status_message

post_parser = reqparse.RequestParser()
post_parser.add_argument('client', type=str)
post_parser.add_argument('session', type=str)
post_parser.add_argument('id', type=str)
post_parser.add_argument('class', type=str)
post_parser.add_argument('name', type=str)
post_parser.add_argument('value', type=str)
post_parser.add_argument('parent', type=dict)
post_parser.add_argument('type', type=str)
post_parser.add_argument('path', type=str)
post_parser.add_argument('method', type=str)
post_parser.add_argument('timestamp', type=int)
post_parser.add_argument('position', type=int)

parser = reqparse.RequestParser()
parser.add_argument('actions', type=str)


class Action(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']

    @jwt_required
    def get(self):
        return self.es.search('actions', 'action', {
            'sort': {
                'timestamp': {'order': 'desc'}
            }
        })['hits']['hits']

    # @jwt_required
    # def get(self, error_id):
    #     return self.es.search('actions', 'action', {
    #         'query': {
    #             'match': {
    #                 'error_id': error_id
    #             }
    #         },
    #         'sort': {
    #             'timestamp': { 'order': 'asc'}
    #         }
    #     })['hits']['hits']

    @jwt_required
    def post(self):
        args = parser.parse_args()
        actions = json.loads(args['actions'])

        for action in actions:
            self.es.index('actions', 'action', action)

        return http_status_message(200)
        # return self.es.index('actions', 'action', post_parser.parse_args())
