import os
from .base import *

ENVIRONMENT = os.environ["DJANGO_ENVIRONMENT"]

if ENVIRONMENT == "production":
    from .production import *
# elif ENVIRONMENT == "staging":
#     from staging import *
elif ENVIRONMENT == "development":
    from .dev import *
else:
    raise RuntimeError("Settings ENVIRONMENT variable not configured correctly!")
