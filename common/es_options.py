from flask_restful import reqparse

optsParser = reqparse.RequestParser()
optsParser.add_argument('reverse', type=bool, location='args')


class EsOptions(object):

    def __init__(self):
        self.esOpts = {}
        self.matches = {}
        self.filters = {}
        self.setPaging()

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

    def addFilter(self, key, value: str):
        if not value is None:
            type = 'must_not' if value.startswith('!') else 'filter'  # 'must'
            self.__addKeyIfNotExists__(self.filters, type)
            self.__addKeyIfNotExists__(self.filters[type], 'match')
            self.filters[type]['match'][key] = value.replace('!', '')

    def get(self):
        if self.matches:
            self.__addKeyIfNotExists__(self.esOpts, 'query')
            self.esOpts['query']['match'] = self.matches

        if self.filters:
            self.__addKeyIfNotExists__(self.esOpts, 'query')
            self.__addKeyIfNotExists__(self.esOpts['query'], 'bool')
            self.esOpts['query']['bool'] = self.filters

        return self.esOpts

    def __addKeyIfNotExists__(self, dict: dict, key):
        if not key in dict:
            dict[key] = {}
