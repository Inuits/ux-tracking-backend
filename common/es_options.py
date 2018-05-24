from flask_restful import reqparse

queryParser = reqparse.RequestParser()
queryParser.add_argument('client', type=str, location='args')
queryParser.add_argument('session', type=str, location='args')

optsParser = reqparse.RequestParser()
optsParser.add_argument('reverse', type=bool, location='args')

class EsOptions(object):

    def __init__(self):
        self.esOpts = {}
        self.matches = {}
        self.setPaging()

        params = queryParser.parse_args()
        for key, value in params.items():
            self.addQuery(key, value)

        reverse = optsParser.parse_args()['reverse']
        self.setDefaultSorting(reverse)

    def setPaging(self):
        paging = reqparse.RequestParser()
        paging.add_argument('limit', type=int, location='args')
        paging.add_argument('from', type=int, location='args')

        args = paging.parse_args()
        self.esOpts['size'] = args['limit'] if not args['limit'] is None else 100
        self.esOpts['from'] = args['from'] if not args['from'] is None else 0

    def setSorting(self, sortingmethod):
        self.esOpts['sort'] = sortingmethod

    def setDefaultSorting(self, reverse=False):
        if not reverse:
            self.setSorting({
                'timestamp': {'order': 'desc'}
            })
        else:
            self.setSorting({
                'timestamp': {'order': 'asc'}
            })

    def addQuery(self, key, value):
        if not value is None:
            self.matches[key] = value

    def get(self):
        if self.matches:
            self.esOpts['query'] = {
                'match': self.matches
            }

        return self.esOpts
