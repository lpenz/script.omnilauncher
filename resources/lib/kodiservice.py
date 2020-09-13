"""Kodi service that is injected into the omnilauncher client"""

import xbmcgui
import xbmcplugin

from resources.lib.log import getLogger

log = getLogger(__name__)


class KodiService(object):
    def __init__(self, handle):
        log.info("KodiService handle %d", handle)
        self.handle = handle

    def getSetting(self, *args, **kwargs):  # noqa: N802
        return xbmcplugin.getSetting(self.handle, *args, **kwargs)

    def listItem(self, *args, **kwargs):  # noqa: N802
        return xbmcgui.ListItem(*args, **kwargs)

    def setInfo(self, li, *args, **kwargs):  # noqa: N802
        return li.setInfo(*args, **kwargs)

    def setArt(self, li, *args, **kwargs):  # noqa: N802
        return li.setArt(*args, **kwargs)

    def addDirectoryItem(self, *args, **kwargs):  # noqa: N802
        return xbmcplugin.addDirectoryItem(self.handle, *args, **kwargs)

    def endOfDirectory(self, *args, **kwargs):  # noqa: N802
        return xbmcplugin.endOfDirectory(self.handle, *args, **kwargs)

    def notification(self, *args, **kwargs):
        xbmcgui.Dialog().notification("omnilauncher error", *args, **kwargs)
