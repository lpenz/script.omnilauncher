'''Kodi service that is injected into the omnilauncher client'''

import xbmcgui
import xbmcplugin


class KodiService(object):

    def __init__(self, handle):
        self.handle = handle

    def getSetting(self, name):
        return xbmcplugin.getSetting(self.handle, name)

    def listItem(self, text):
        return xbmcgui.ListItem(text)

    def setInfo(self, li, name, nfo):
        return li.setInfo(name, nfo)

    def setArt(self, li, art):
        return li.setArt(art)

    def addDirectoryItem(self, uri, li, isFolder=False):
        return xbmcplugin.addDirectoryItem(self.handle,
                                           uri, li, isFolder=False)

    def endOfDirectory(self):
        return xbmcplugin.endOfDirectory(self.handle)

    def notification(self, msg):
        xbmcgui.Dialog().notification('omnilauncher error', msg)
