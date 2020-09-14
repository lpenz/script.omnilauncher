"""
Core code of omnilauncher

To ease testing, we inject kodi API as a service.
The official code is in kodiservice.py.
"""

import os
from resources.lib.log import getLogger

try:
    import urllib.parse as urlencodemodule
except ImportError:
    import urllib as urlencodemodule

import subprocess
import xml.etree.ElementTree as Xmltree


pj = os.path.join
log = getLogger(__name__)


class Omnilauncher(object):
    def __init__(self, kodi):
        self.kodi = kodi

    def run(self, uri, args):
        self.uri = uri
        if not args or "type" not in args:
            try:
                root = self.kodi.getSetting("root")
            except Exception:
                self.kodi.notification(
                    "Please configure collection root path in settings"
                )
                raise
            self.directory_render(root)
        elif args["type"][0] == "shell":
            cmd = "cd {}; {}".format(args["path"][0], args["target"][0])
            log.info("shell start: {}".format(cmd))
            subprocess.check_call(args["target"][0], cwd=args["path"][0],
                                  shell=True)
            log.info("shell  done: {}".format(cmd))
        elif args["type"][0] == "directory":
            path = pj(args["path"][0], args["target"][0])
            log.debug("directory render: {}".format(path))
            self.directory_render(path)
        else:
            raise KeyError("unknown type {}".format(args["type"][0]))

    def directory_render(self, path):
        for filebase in os.listdir(path):
            filename = pj(path, filebase)
            if not filename.endswith(".xml"):
                continue
            try:
                et = Xmltree.parse(filename)
            except Exception as e:
                log.warn(str((filename, e)))
                continue
            root = et.getroot()
            if root.tag != "omnilauncher":
                continue
            self.item_add(path, filename, et)
        self.kodi.endOfDirectory()

    def item_add(self, path, filename, et):
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
                art[etfield.tag] = pj(path, etfield.text)
        if len(art) > 0:
            self.kodi.setArt(li, art)
        # The first <target> is the menu action
        target = next(et.iter("target"))
        typ = target.get("type")
        uridict = {"type": typ, "path": path, "target": target.text}
        isfolder = typ == "directory"
        log.debug("addDirectoryItem {}, isFolder={}".format(uridict, isfolder))
        uri = self.uri + "?" + urlencodemodule.urlencode(uridict)
        self.kodi.addDirectoryItem(url=uri, listitem=li, isFolder=isfolder)
