import doctest
import os
import unittest

import core
from core import app, db

#os.environ['CONFIG'] = 'tests.test_config'

app.config['TESTING'] = True
app.config['CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'thisismyscretkey'
app.config['WTF_CSRF_ENABLED'] = False
BASE_DIR = app.config.get("BASE_DIR")


class HubytTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(HubytTests, self).__init__(*args, **kwargs)
        self.client = app.test_client()
        #utils.init(core)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_doctests(self):
        modules = [utils]
        for mod in modules:
            failed, tests = doctest.testmod(mod)
            if failed:
                raise Exception("Failed a doctest")


if __name__ == '__main__':
    unittest.main()
