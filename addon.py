'''Omnilauncher entry point'''

import sys
try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

if (__name__ == "__main__"):
    import resources.lib.omnilauncher
    resources.lib.omnilauncher.main(
        sys.argv[0], int(sys.argv[1]), parse_qs(sys.argv[2][1:]))
