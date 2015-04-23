from nose.tools import *
from jadi import *


@service
class TestService(object):
    def __init__(self, context):
        pass


@interface
class TestInterface(object):
    def __init__(self, context):
        pass


@interface
class TestInterface2(object):
    def __init__(self, context):
        pass


@component(TestInterface)
class TestComponent(object):
    def __init__(self, context):
        pass


@component(TestInterface)
class TestComponent2(object):
    def __init__(self, context):
        pass


@component(TestInterface)
class TestComponent3(object):
    def __init__(self, context):
        pass

    @classmethod
    def __verify__(cls):
        return False


def fqdn_test():
    class Test:
        pass

    eq_(get_fqdn(Test), 'tests.Test')


def service_test():
    ctx = Context()
    assert isinstance(TestService.get(ctx), TestService)
    eq_(TestService.get(ctx), TestService.get(ctx))


def component_test():
    ctx = Context()
    all = TestInterface.all(ctx)
    eq_(len(all), 2)
    assert isinstance(all[0], TestComponent)
    assert isinstance(all[1], TestComponent2)
    any = TestInterface.any(ctx)
    assert isinstance(any, TestComponent)
    assert isinstance(TestComponent.get(ctx), TestComponent)


@raises(NoImplementationError)
def exc_test():
    TestInterface2.any(Context())
