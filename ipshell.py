import IPython

from finone.api import *
from finone.models import *
from finone.utils import *
from finone.constants import *
from finone.exceptions import *
from finone.routes import *
from finone.serializers import *
from finone.parsers import *


welcome = \
"""
Welcome to Financial One iPython shell!

You have access to the following app commands:
* migrate
* app
* marshmallow
* api
* db

All module objects have been imported.
"""
IPython.embed(header=welcome)