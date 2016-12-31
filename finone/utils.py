import re

first_cap_re = re.compile('(.)([A-Z][a-z])')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_to_underscore(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def underscoreize(data):
    """
    Recursively convert camelcase data to underscore
    Requires all dictionary keys to be strings
    """
    global camel_to_underscore
    if isinstance(data, dict):
        retval = {camel_to_underscore(key): underscoreize(value)
                  for key, value in data.items()}
    elif isinstance(data, (list, tuple)):
        retval = [underscoreize(item) for item in data]
    else:
        retval = data
    return retval
