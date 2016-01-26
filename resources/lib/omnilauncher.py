'''Core code of omnilauncher'''

import os
try:
    import urllib as urlencodemodule
except ImportError:
    import urllib.parse as urlencodemodule

import subprocess
import xbmcgui
import xbmcplugin
import xml.etree.ElementTree as xmltree

pj = os.path.join

URI_TOP = u'plugin://script.omnilauncher/'


class Omnilauncher(object):

    def __init__(self, handle):
        self.handle = handle
        self.home = xbmcplugin.getSetting(handle, 'home')

    def run(self, uri, args):
        if len(args) == 0:
            self.top(uri, args)
            return
        if 'command' in args:
            subprocess.call(args['command'], shell=True)

    def top(self, uri, args):
        for d in os.listdir(self.home):
            self.item_add(pj(self.home, d, 'omniitem.nfo'))
        xbmcplugin.endOfDirectory(self.handle)

    def item_add(self, itemfile):
        try:
            et = xmltree.parse(itemfile)
        except Exception:
            return
        li = xbmcgui.ListItem(et.find('./title').text)
        nfo = {}
        for etinfo in et.iter('info'):
            for etfield in etinfo.iter():
                if etfield == etinfo:
                    continue
                nfo[etfield.tag] = etfield.text
        li.setInfo('video', nfo)
        art = {}
        for etart in et.iter('art'):
            for etfield in etart.iter():
                if etfield == etart:
                    continue
                art[etfield.tag] = pj(
                    os.path.dirname(itemfile),
                    etfield.text)
        li.setArt(art)
        for target in et.iter('target'):
            if target.get('type') == 'command':
                uri = URI_TOP + '?' + \
                    urlencodemodule.urlencode(
                        {
                            'itemfile': itemfile,
                            'command': target.text
                        })
                xbmcplugin.addDirectoryItem(
                    self.handle, uri, li, isFolder=False)


def main(uri, handle, args):
    o = Omnilauncher(handle)
    o.run(uri, args)
