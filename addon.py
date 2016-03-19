'''Omnilauncher entry point'''

import sys
import logging
try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

from resources.lib import omnilauncher
from resources.lib import kodiservice


def _log():
    if _log.logger is None:
        logging.basicConfig()
        _log.logger = logging.getLogger(__name__)
    return _log.logger
_log.logger = None


def main():
    _log().debug(sys.argv)
    uri = sys.argv[0]
    handle = int(sys.argv[1])
    args = parse_qs(sys.argv[2][1:])
    kodi = kodiservice.KodiService(handle)
    o = omnilauncher.Omnilauncher(kodi)
    o.run(uri, args)

if __name__ == "__main__":
    main()
