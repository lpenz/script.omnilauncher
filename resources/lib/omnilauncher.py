'''Core code of omnilauncher

To ease testing, we inject kodi API as a service.
The official code is in kodiservice.py.
'''

import os
try:
    import urllib as urlencodemodule
except ImportError:
    import urllib.parse as urlencodemodule

import subprocess
import xml.etree.ElementTree as xmltree

pj = os.path.join

URI_TOP = u'plugin://script.omnilauncher/'


class Omnilauncher(object):

    def __init__(self, kodi):
        self.kodi = kodi
        self.home = kodi.getSetting('home')

    def run(self, uri, args):
        if len(args) == 0:
            self.top(uri, args)
            return
        if 'command' in args:
            subprocess.call(args['command'], shell=True)

    def top(self, uri, args):
        for d in os.listdir(self.home):
            self.item_add(pj(self.home, d, 'omniitem.nfo'))
        self.kodi.endOfDirectory()

    def item_add(self, itemfile):
        try:
            et = xmltree.parse(itemfile)
        except Exception:
            return
        li = self.kodi.listItem(et.find('./title').text)
        nfo = {}
        for etinfo in et.iter('info'):
            for etfield in etinfo.iter():
                if etfield == etinfo:
                    continue
                nfo[etfield.tag] = etfield.text
        self.kodi.setInfo(li, 'video', nfo)
        art = {}
        for etart in et.iter('art'):
            for etfield in etart.iter():
                if etfield == etart:
                    continue
                art[etfield.tag] = pj(
                    os.path.dirname(itemfile),
                    etfield.text)
        self.kodi.setArt(li, art)
        for target in et.iter('target'):
            if target.get('type') == 'command':
                uri = URI_TOP + '?' + \
                    urlencodemodule.urlencode(
                        {
                            'itemfile': itemfile,
                            'command': target.text
                        })
                self.kodi.addDirectoryItem(
                    uri, li, isFolder=False)
