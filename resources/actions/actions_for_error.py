from flask_jwt_extended import jwt_required
from flask_restful import Resource

from common.es_options import EsOptions


class ActionsForError(Resource):
    def __init__(self, **kwargs):
        self.es = kwargs['es']

    @jwt_required
    def get(self, error_id):
        esOpts = EsOptions()
        esOpts.addQuery('error_id', error_id)

        actions = self.es.search('actions', 'action', esOpts.get())

        return actions['hits'] if 'hits' in actions else []
