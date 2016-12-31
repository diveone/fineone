from finone import *
import IPython


welcome = \
"""
Welcome to Financial One iPython shell!

You have access to the following app commands:
* migrate
* app
* marshmallow
* api
* db

To import objects from the modules: finone.module_name
"""
IPython.embed(header=welcome)