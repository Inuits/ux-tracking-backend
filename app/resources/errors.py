from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields
from rest_framework import status

from app.resources.ux_resource import UxResource

error_fields = {
    'error': fields.String,
    'source': fields.String,
    'position': fields.String,
    'stack': fields.String,
}

post_parser = reqparse.RequestParser()
post_parser.add_argument('client', type=str)
post_parser.add_argument('session', type=str)
post_parser.add_argument('error', type=str)
post_parser.add_argument('source', type=str)
post_parser.add_argument('position', type=str)
post_parser.add_argument('stack', type=str)
post_parser.add_argument('timestamp', type=int)


class Errors(UxResource):
    def __init__(self, **kwargs):
        super().__init__()
        self.es = kwargs['es']

    @jwt_required
    def get(self, error_id=None):
        statusCode = status.HTTP_200_OK

        if error_id is not None:
            self.esOpts.addFilter('_id', error_id)

        try:
            errors = self.es.search('errors', 'error', self.esOpts.get())

        except:
            return [], status.HTTP_204_NO_CONTENT

        return errors['hits'] if 'hits' in errors else [], statusCode

    @jwt_required
    def post(self):
        args = post_parser.parse_args()
        self.es.index('errors', 'error', args)

        return {}, status.HTTP_201_CREATED
