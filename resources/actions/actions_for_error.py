from flask_jwt_extended import jwt_required
from flask_restful import Resource


class ActionsForError(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']

    @jwt_required
    def get(self, error_id):
        return self.es.search('actions', 'action', {
            'query': {
                'match': {
                    'error_id': error_id
                }
            },
            'sort': {
                'timestamp': {'order': 'asc'}
            }
        })['hits']['hits']
