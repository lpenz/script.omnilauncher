'''Core code of omnilauncher'''

import os
import xbmcgui
import xbmcplugin
import xml.etree.ElementTree as xmltree

pjoin = os.path.join


class Omnilauncher(object):

    def __init__(self, handle):
        self.handle = handle
        self.home = xbmcplugin.getSetting(handle, 'home')

    def run(self):
        for d in os.listdir(self.home):
            nfofile = pjoin(self.home, d, 'collection.nfo')
            try:
                et = xmltree.parse(nfofile)
            except Exception:
                continue
            li = xbmcgui.ListItem(et.find('./title').text)
            nfo = {}
            for field in ['year', 'plot']:
                i = et.find('./' + field)
                if i:
                    nfo[field] = i
            li.setInfo('video', nfo)
            art = {}
            for field in ['fanart', 'thumb']:
                i = et.find('./' + field)
                if i is not None:
                    art[field] = pjoin(self.home, d, i.text)
            li.setArt(art)
            xbmcplugin.addDirectoryItem(self.handle, u'', li)
        xbmcplugin.endOfDirectory(self.handle)


def main(handle):
    o = Omnilauncher(handle)
    o.run()
