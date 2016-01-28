'''Core code of omnilauncher

To ease testing, we inject kodi API as a service.
The official code is in kodiservice.py.
'''

import os
import logging
try:
    import urllib as urlencodemodule
except ImportError:
    import urllib.parse as urlencodemodule

import subprocess
from glob import glob
import xml.etree.ElementTree as xmltree

pj = os.path.join

URI_TOP = u'plugin://script.omnilauncher/'


def _log():
    if _log.logger is None:
        logging.basicConfig()
        _log.logger = logging.getLogger(__name__)
    return _log.logger
_log.logger = None


class Omnilauncher(object):

    def __init__(self, kodi):
        self.kodi = kodi
        try:
            self.root = kodi.getSetting('root')
        except:
            self.root = ''

    def run(self, uri, args):
        if self.root == '':
            self.kodi.notification(
                'Please configure root omniitem in settings')
            return
        if len(args) == 0:
            self.menu_render(self.root)
        elif args['type'][0] == 'command':
            subprocess.call(args['target'], shell=True)

    def menu_render(self, itemfile):
        try:
            et = xmltree.parse(itemfile)
        except Exception as e:
            _log().warn(str(e))
            return
        basepath = os.path.dirname(itemfile)
        for target in et.iter('target'):
            if target.get('type') == 'glob':
                for f in glob(pj(basepath, target.text)):
                    self.item_add(f)
        self.kodi.endOfDirectory()

    def item_add(self, itemfile):
        try:
            et = xmltree.parse(itemfile)
        except Exception as e:
            _log().warn(str(e))
            return
        li = self.kodi.listItem(et.find('./title').text)
        nfo = {}
        for etinfo in et.iter('info'):
            for etfield in etinfo.iter():
                if etfield == etinfo:
                    continue
                nfo[etfield.tag] = etfield.text
        if len(nfo) > 0:
            self.kodi.setInfo(li, 'video', nfo)
        art = {}
        for etart in et.iter('art'):
            for etfield in etart.iter():
                if etfield == etart:
                    continue
                art[etfield.tag] = pj(
                    os.path.dirname(itemfile),
                    etfield.text)
        if len(art) > 0:
            self.kodi.setArt(li, art)
        # The first target is the menu action
        target = next(et.iter('target'))
        isFolder = target.get('type') != 'command'
        uridict = {'itemfile': itemfile,
                   'type': target.get('type'),
                   'target': target.text}
        uri = URI_TOP + '?' + urlencodemodule.urlencode(uridict)
        self.kodi.addDirectoryItem(
            uri, li, isFolder=isFolder)
