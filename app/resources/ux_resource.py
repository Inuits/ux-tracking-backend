from flask_restful import Resource, reqparse

from app.common.es_options import EsOptions

optsParser = reqparse.RequestParser()
optsParser.add_argument('reverse', type=str, location='args')

paging = reqparse.RequestParser()
paging.add_argument('limit', type=int, location='args')
paging.add_argument('from', type=int, location='args')


class UxResource(Resource):
    def __init__(self):
        self.esOpts = EsOptions()
        args = optsParser.parse_args()
        self.esOpts.setDefaultSorting(args['reverse'] == 'true')

        args = paging.parse_args()
        self.esOpts.setPaging(args['limit'] if not args['limit'] is None else 100,
                              args['from'] if not args['from'] is None else 0)
