'''Omnilauncher entry point'''

import sys

if (__name__ == "__main__"):
    import resources.lib.omnilauncher
    resources.lib.omnilauncher.main(int(sys.argv[1]))
