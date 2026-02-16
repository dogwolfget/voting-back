from .base import *  # noqa

DEBUG = True
THIRD_PARTY_APPS += ['debug_toolbar']  # noqa
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa
