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
            itemfile = pjoin(self.home, d, 'omniitem.nfo')
            try:
                et = xmltree.parse(itemfile)
            except Exception:
                continue
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
                    art[etfield.tag] = pjoin(self.home, d, etfield.text)
            li.setArt(art)
            xbmcplugin.addDirectoryItem(self.handle, u'', li)
        xbmcplugin.endOfDirectory(self.handle)


def main(handle):
    o = Omnilauncher(handle)
    o.run()
