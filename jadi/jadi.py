from .common import log, get_fqdn


class Context(object):
    '''
    An IoC container for :func:`interface` s, :func:`service` s and :func:`component` s

    :param parent: a parent context
    :type parent: :class:`Context`
    '''

    def __init__(self, parent=None):
        self.parent = parent
        self.service_instances = {}
        self.component_instances = {}

    def __repr__(self):
        if self.parent:
            return '[Context %s (child of %s)]' % (id(self), id(self.parent))
        else:
            return '[Context %s]' % id(self)

    def get_service(self, cls):
        fqdn = get_fqdn(cls)
        if fqdn not in self.service_instances:
            self.service_instances[fqdn] = cls(self)
        return self.service_instances[fqdn]

    def get_component(self, cls):
        fqdn = get_fqdn(cls)
        if fqdn not in self.component_instances:
            self.component_instances[fqdn] = cls(self)
        return self.component_instances[fqdn]

    def get_components(self, cls):
        for comp in cls.implementations:
            yield self.get_component(comp)


def service(cls):
    '''
    Marks the decorated class as a singleton ``service``.

    Injects following classmethods:

        .. py:method:: .get(context)

            Returns a singleton instance of the class for given ``context``

            :param context: context to look in
            :type context: :class:`Context`
            :returns: ``cls``
    '''

    if not cls:
        return None

    # Inject methods
    def get(cls, context):
        return context.get_service(cls)
    cls.get = get.__get__(cls)

    log.debug('Registering [%s] (service)', get_fqdn(cls))

    return cls


class NoImplementationError(Exception):
    def __init__(self, cls):
        self.cls = cls

    def __str__(self):
        return u'No implementation for [%s] is available' % self.cls.__name__

    def __repr__(self):
        return unicode(self)


def interface(cls):
    '''
    Marks the decorated class as an abstract interface.

    Injects following classmethods:

        .. py:method:: .all(context) 

            Returns a list of instances of each component in the ``context`` implementing this ``@interface``

            :param context: context to look in
            :type context: :class:`Context`
            :returns: list(``cls``)

        .. py:method:: .any(context)

            Returns the first suitable instance implementing this ``@interface`` or raises :exc:`NoImplementationError` if none is available.

            :param context: context to look in
            :type context: :class:`Context`
            :returns: ``cls``

        .. py:method:: .classes()

            Returns a list of classes implementing this ``@interface``

            :returns: list(class)
    '''

    if not cls:
        return None

    cls.implementations = []

    # Inject methods
    def _all(cls, context):
        return list(context.get_components(cls))
    cls.all = _all.__get__(cls)

    def _any(cls, context):
        instances = cls.all(context)
        if instances:
            return instances[0]
        raise NoImplementationError(cls)
    cls.any = _any.__get__(cls)

    def _classes(cls):
        return list(cls.implementations)
    cls.classes = _classes.__get__(cls)

    log.debug('Registering [%s] (interface)', get_fqdn(cls))

    return cls


def component(iface):
    '''
    Marks the decorated class as a component implementing the given ``iface``

    :param iface: the interface to implement
    :type iface: :func:`interface`
    '''

    def decorator(cls):
        if not cls:
            return None

        # Run custom verificator if any
        if hasattr(cls, '__verify__'):
            if not cls.__verify__():
                return cls

        if not hasattr(iface, 'implementations'):
            log.error('%s is not an @interface', iface)

        log.debug(
            'Registering [%s] (implementation of [%s])' % (
                get_fqdn(cls),
                get_fqdn(iface)
            )
        )
        iface.implementations.append(cls)

        def get(cls, context):
            return context.get_component(cls)
        cls.get = get.__get__(cls)

        return cls

    return decorator
