"""Omnilauncher unit tests"""


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

    def getSetting(self, name):  # noqa: N802
        return self.settings[name]

    def listItem(self, text):  # noqa: N802
        li = {"text": text}
        return li

    def setInfo(self, li, name, nfo):  # noqa: N802
        li[name] = nfo

    def setArt(self, li, art):  # noqa: N802
        li["art"] = art

    def addDirectoryItem(self, uri, listitem,
                         isFolder=False):  # noqa: N802,N803
        self.directory_tmp[uri] = (listitem, isFolder)

    def endOfDirectory(self):  # noqa: N802
        self.directory = self.directory_tmp

    def notification(self, msg):  # noqa: N802
        self.notifications.append(msg)


def tmpwritexml(txt):
    tmp = tempfile.NamedTemporaryFile(suffix=".xml")
    tmp.write(b"""<?xml version='1.0' encoding='UTF-8'?>""")
    tmp.write(txt.encode("utf-8"))
    tmp.flush()
    return tmp


# Tests:


class TestOmnilauncher(unittest.TestCase):
    def mock_with_root(self, xml):
        tmp = tmpwritexml(xml)
        mock = MockService({"root": tmp.name, "tmp": tmp})
        # (tmp in settings prevents the gc from collecting it
        # and deleting the file)
        return mock

    def test_instance(self):
        """No exception is raised"""
        omnilauncher.Omnilauncher(MockService())

    def test_no_root(self):
        """Notify if no root configured"""
        m = MockService()
        o = omnilauncher.Omnilauncher(m)
        # with no root, it should have print a notification and raise
        with self.assertRaises(Exception):
            o.run("", {})
        self.assertTrue(len(m.notifications) > 0)
