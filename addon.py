"""Omnilauncher entry point"""

import sys
from resources.lib.log import getLogger

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

from resources.lib import omnilauncher
from resources.lib import kodiservice

log = getLogger(__name__)


def main():
    log.debug(sys.argv)
    uri = sys.argv[0]
    handle = int(sys.argv[1])
    args = parse_qs(sys.argv[2][1:])
    log.debug("uri {} handle {} args {}".format(uri, handle, args))
    kodi = kodiservice.KodiService(handle)
    o = omnilauncher.Omnilauncher(kodi)
    o.run(uri, args)


if __name__ == "__main__":
    main()
