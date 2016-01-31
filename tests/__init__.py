'''Omnilauncher unit tests'''

import tempfile
import unittest

from resources.lib import omnilauncher  # NOQA


# Mock:

class MockService(object):

    def __init__(self, settings={}):
        self.settings = settings
        self.directory_tmp = {}
        self.directory = {}
        self.notifications = []

    def getSetting(self, name):
        return self.settings[name]

    def listItem(self, text):
        li = {'text': text}
        return li

    def setInfo(self, li, name, nfo):
        li[name] = nfo

    def setArt(self, li, art):
        li['art'] = art

    def addDirectoryItem(self, uri, li, isFolder=False):
        self.directory_tmp[uri] = (li, isFolder)

    def endOfDirectory(self):
        self.directory = self.directory_tmp

    def notification(self, msg):
        self.notifications.append(msg)


def tmpwritexml(txt):
    tmp = tempfile.NamedTemporaryFile(suffix='.xml')
    tmp.write(b'''<?xml version='1.0' encoding='UTF-8'?>''')
    tmp.write(txt.encode('utf-8'))
    tmp.flush()
    return tmp

# Tests:


class TestOmnilauncher(unittest.TestCase):

    def mock_with_root(self, xml):
        tmp = tmpwritexml(xml)
        mock = MockService({'root': tmp.name, 'tmp': tmp})
        # (tmp in settings prevents the gc from collecting it
        # and deleting the file)
        return mock

    def test_instance(self):
        '''No exception is raised'''
        omnilauncher.Omnilauncher(MockService())

    def test_no_root(self):
        '''Notify if no root configured'''
        m = MockService()
        o = omnilauncher.Omnilauncher(m)
        # with no root, it should have printed a notification
        o.run('', {})
        self.assertTrue(len(m.notifications) > 0)

    def test_root_glob(self):
        '''Test single-file glob'''
        tmp = tmpwritexml(u'''
            <omniitem>
              <title>item1</title>
              <target type="command">echo 1</target>
            </omniitem>
        ''')
        m = self.mock_with_root(u'''
            <omniitem>
                <target type="glob">{}</target>
            </omniitem>
        '''.format(tmp.name))
        o = omnilauncher.Omnilauncher(m)
        o.run('', [])
        self.assertEqual(
            list(m.directory.values()),
            [({'text': 'item1'}, False)])
