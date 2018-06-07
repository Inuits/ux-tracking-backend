class EsOptions(object):

    def __init__(self):
        self.esOpts = {}
        self.filters = {'include': {}, 'exclude': {}}

    def setPaging(self, size, fromval=0):
        self.esOpts['size'] = size
        self.esOpts['from'] = fromval

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

    def addFilter(self, key: str, value: str):
        if not value is None:
            if ',' in value:
                for val in value.split(','):
                    self.addFilter(key, val)
            else:
                incType = 'exclude' if value.startswith('!') else 'include'
                if not key in self.filters[incType]:
                    self.filters[incType][key] = []

                self.filters[incType][key].append(value[1:] if value.startswith('!') else value)

    def get(self):
        if self.filters['include'] or self.filters['exclude']:
            self.__addKeyIfNotExists__(self.esOpts, 'query')
            self.esOpts['query']['bool'] = {'must': [], 'must_not': []}
            self.esOpts['query']['bool']['must'].append({'bool': {'should': []}})

            for key, value in self.filters['include'].items():
                self.__addFilter__('must', key, value)

            for key, value in self.filters['exclude'].items():
                self.__addFilter__('must_not', key, value)

        return self.esOpts

    def __addFilter__(self, type, key, value):
        if len(value) == 1:
            self.esOpts['query']['bool'][type].append(self.__getFilterTerm__(key, value[0]))
            return

        for item in value:
            if type is 'must':
                self.esOpts['query']['bool'][type][0]['bool']['should'].append(self.__getFilterTerm__(key, item))
            else:
                self.esOpts['query']['bool'][type].append(self.__getFilterTerm__(key, item))

    def __getFilterTerm__(self, key, value):
        if '*' in value:
            return {'wildcard': {key: value}}
        else:
            return {'term': {key: value}}

    def __addKeyIfNotExists__(self, dict: dict, key):
        if not key in dict:
            dict[key] = {}
