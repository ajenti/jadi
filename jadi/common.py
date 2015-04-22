import logging

log = logging.getLogger('jadi')


def get_fqdn(cls):
    '''
    Returns a fully-qualified name for the given class
    '''
    return cls.__module__ + '.' + cls.__name__
