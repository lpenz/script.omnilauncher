'''Kodi service that is injected into the omnilauncher client'''

import xbmcgui
import xbmcplugin


class KodiService(object):

    def __init__(self, handle):
        self.handle = handle

    def getSetting(self, *args, **kwargs):
        return xbmcplugin.getSetting(self.handle, *args, **kwargs)

    def listItem(self, *args, **kwargs):
        return xbmcgui.ListItem(*args, **kwargs)

    def setInfo(self, li, *args, **kwargs):
        return li.setInfo(*args, **kwargs)

    def setArt(self, li, *args, **kwargs):
        return li.setArt(*args, **kwargs)

    def addDirectoryItem(self, *args, **kwargs):
        return xbmcplugin.addDirectoryItem(self.handle, *args, **kwargs)

    def endOfDirectory(self, *args, **kwargs):
        return xbmcplugin.endOfDirectory(self.handle, *args, **kwargs)

    def notification(self, *args, **kwargs):
        xbmcgui.Dialog().notification('omnilauncher error', *args, **kwargs)
