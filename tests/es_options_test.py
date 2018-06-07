import unittest

from app.common.es_options import EsOptions


class EsOptionsTest(unittest.TestCase):

    def setUp(self):
        self.options = EsOptions()

    def testOptionsIsNotNone(self):
        self.assertIsNotNone(self.options)

    def testOptionsSetPaging(self):
        self.assertNotIn('size', self.options.get())

        self.options.setPaging(10, 20)

        self.assertIn('size', self.options.get())
        self.assertIn('from', self.options.get())

        self.assertEqual(10, self.options.get()['size'])
        self.assertEqual(20, self.options.get()['from'])

    def testOptionsSetOrder(self):
        self.assertNotIn('sort', self.options.get())

        self.options.setDefaultSorting(reverse=True)
        self.assertIn('sort', self.options.get())
        self.assertIn('timestamp', self.options.get()['sort'])
        self.assertIn('order', self.options.get()['sort']['timestamp'])
        self.assertEqual('asc', self.options.get()['sort']['timestamp']['order'])

        self.options.setDefaultSorting()
        self.assertEqual('desc', self.options.get()['sort']['timestamp']['order'])

    def testOptionsFilterOneTerm(self):
        self.assertEqual(0, len(self.options.get()))

        self.options.addFilter('error_id', 'testid')

        options = self.options.get()
        self.assertIn('query', options)
        self.assertIn('bool', options['query'])
        self.assertIn('must', options['query']['bool'])
        self.assertEqual(2, len(options['query']['bool']['must']))  # 'must' automatically includes 'should'
        self.assertEqual('testid', options['query']['bool']['must'][1]['term']['error_id'])

    def testOptionsFilterTwoSameTerms(self):
        self.options.addFilter('method', 'click,focusout')

        options = self.options.get()
        self.assertIn('query', options)
        self.assertEqual(1, len(options['query']['bool']['must']))
        self.assertIn('bool', options['query']['bool']['must'][0])
        self.assertEqual(2, len(options['query']['bool']['must'][0]['bool']['should']))
        self.assertEqual('click', options['query']['bool']['must'][0]['bool']['should'][0]['term']['method'])
        self.assertEqual('focusout', options['query']['bool']['must'][0]['bool']['should'][1]['term']['method'])

    def testOptionsFilterExclude(self):
        self.options.addFilter('method', '!req')

        options = self.options.get()
        self.assertIn('must_not', options['query']['bool'])
        self.assertEqual(1, len(options['query']['bool']['must_not']))
        self.assertEqual('req', options['query']['bool']['must_not'][0]['term']['method'])

    def testOptionsFilterExcludeMultiple(self):
        self.options.addFilter('method', '!req,!click')

        options = self.options.get()
        self.assertIn('must_not', options['query']['bool'])
        self.assertEqual(2, len(options['query']['bool']['must_not']))
        self.assertEqual('req', options['query']['bool']['must_not'][0]['term']['method'])
        self.assertEqual('click', options['query']['bool']['must_not'][1]['term']['method'])

    def testOptionsFilterIncludeAndExcludeForSameTerm(self):
        self.options.addFilter('method', 'req,!click')

        options = self.options.get()
        self.assertEqual('click', options['query']['bool']['must_not'][0]['term']['method'])
        self.assertEqual('req', options['query']['bool']['must'][1]['term']['method'])

    def testOptionsFiltersIncludeMultiple(self):
        self.options.addFilter('method', 'req')
        self.options.addFilter('client', 'testClient')

        options = self.options.get()
        self.assertEqual('req', options['query']['bool']['must'][1]['term']['method'])
        self.assertEqual('testClient', options['query']['bool']['must'][2]['term']['client'])

    def testOptionsFiltersIncludeMultipleWithMultipleSameTerm(self):
        self.options.addFilter('method', 'click,focusout')
        self.options.addFilter('client', 'testClient')

        options = self.options.get()
        self.assertEqual('click', options['query']['bool']['must'][0]['bool']['should'][0]['term']['method'])
        self.assertEqual('focusout', options['query']['bool']['must'][0]['bool']['should'][1]['term']['method'])
        self.assertEqual('testClient', options['query']['bool']['must'][1]['term']['client'])

    def testOptionsFiltersIncludeMultipleWithMultipleSameTermWithExclude(self):
        self.options.addFilter('method', 'click,focusout')
        self.options.addFilter('client', 'testClient')
        self.options.addFilter('session', '!admin')

        options = self.options.get()
        self.assertEqual('click', options['query']['bool']['must'][0]['bool']['should'][0]['term']['method'])
        self.assertEqual('focusout', options['query']['bool']['must'][0]['bool']['should'][1]['term']['method'])
        self.assertEqual('testClient', options['query']['bool']['must'][1]['term']['client'])
        self.assertEqual('admin', options['query']['bool']['must_not'][0]['term']['session'])


    def testOptionsFiltersIncludeWildCard(self):
        self.options.addFilter('session', 'c7990*')
        options = self.options.get()

        self.assertEqual('c7990*', options['query']['bool']['must'][1]['wildcard']['session'])

    def testOptionsFiltersRange(self):
        self.options.addFilter('timestamp', '<120')
        options = self.options.get()

        self.assertEqual('120', options['query']['bool']['must'][1]['range']['timestamp']['lt'])
