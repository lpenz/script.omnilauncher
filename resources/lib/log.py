"""
Logging config

Guarantees that we call logging.basicConfig before any log, as long as
this module is the first one imported.
"""

import logging

logging.basicConfig()  # level=logging.DEBUG

getLogger = logging.getLogger  # noqa
