from .base import *

DEBUG = True

if DEBUG:
    from .dev import *
else:
    from .prod import *
