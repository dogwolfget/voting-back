from .base import *  # noqa

DEBUG = True
DEBUG_TOOLBAR_ENABLED = True
if DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS += ["debug_toolbar"]  # noqa
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa
    INTERNAL_IPS = ["127.0.0.1"]
