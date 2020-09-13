"""Omnilauncher entry point"""

import sys
import logging

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

from resources.lib import omnilauncher
from resources.lib import kodiservice


def main():
    logging.basicConfig()
    logging.debug(sys.argv)
    uri = sys.argv[0]
    handle = int(sys.argv[1])
    args = parse_qs(sys.argv[2][1:])
    kodi = kodiservice.KodiService(handle)
    o = omnilauncher.Omnilauncher(kodi)
    o.run(uri, args)


if __name__ == "__main__":
    main()
