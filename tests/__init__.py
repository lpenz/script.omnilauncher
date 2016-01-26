'''Omnilauncher unit tests'''

import unittest

from resources.lib import omnilauncher  # NOQA


# Mock:

class MockService(object):

    def getSetting(self, name):
        return None


# Tests:

class TestOmnilauncher(unittest.TestCase):

    def test_instance(self):
        omnilauncher.Omnilauncher(MockService())
