"""Core code of omnilauncher

To ease testing, we inject kodi API as a service.
The official code is in kodiservice.py.
"""

import os
import logging

try:
    import urllib.parse as urlencodemodule
except ImportError:
    import urllib as urlencodemodule

import subprocess
from glob import glob
import xml.etree.ElementTree as xmltree

pj = os.path.join


def _log():
    if _log.logger is None:
        logging.basicConfig()
        _log.logger = logging.getLogger(__name__)
    return _log.logger


_log.logger = None


class Omnilauncher(object):
    def __init__(self, kodi):
        self.kodi = kodi

    def run(self, uri, args):
        self.uri = uri
        if len(args) == 0:
            try:
                root = self.kodi.getSetting("root")
            except Exception:
                self.kodi.notification("Please configure root omniitem in settings")
                raise
            self.menu_render(root)
        elif args["type"][0] == "command":
            subprocess.call(args["target"], shell=True)
        else:
            self.menu_render(args["itemfile"][0])

    def menu_render(self, itemfile):
        try:
            et = xmltree.parse(itemfile)
        except Exception as e:
            _log().warn(str(e))
            return
        basepath = os.path.dirname(itemfile)
        for target in et.iter("target"):
            if target.get("type") == "glob":
                for f in glob(pj(basepath, target.text)):
                    self.item_add(f)
        self.kodi.endOfDirectory()

    def item_add(self, itemfile):
        try:
            et = xmltree.parse(itemfile)
        except Exception as e:
            _log().warn(str(e))
            return
        li = self.kodi.listItem(et.find("./title").text)
        nfo = {}
        for etinfo in et.iter("info"):
            for etfield in etinfo.iter():
                if etfield == etinfo:
                    continue
                nfo[etfield.tag] = etfield.text
        if len(nfo) > 0:
            self.kodi.setInfo(li, "video", nfo)
        art = {}
        for etart in et.iter("art"):
            for etfield in etart.iter():
                if etfield == etart:
                    continue
                art[etfield.tag] = pj(os.path.dirname(itemfile), etfield.text)
        if len(art) > 0:
            self.kodi.setArt(li, art)
        # The first target is the menu action
        target = next(et.iter("target"))
        isFolder = target.get("type") != "command"
        uridict = {
            "itemfile": itemfile,
            "type": target.get("type"),
            "target": target.text,
        }
        uri = self.uri + "?" + urlencodemodule.urlencode(uridict)
        self.kodi.addDirectoryItem(uri, li, isFolder=isFolder)
