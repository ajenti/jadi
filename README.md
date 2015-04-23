# Jadi

[![Build Status](https://travis-ci.org/ajenti/jadi.svg)](https://travis-ci.org/ajenti/jadi)

Minimalistic IoC for Python

```python
import os
import subprocess
from jadi import service, component, interface, Context


# @services are singletons within their Context

@service
class FooService(object):
    def __init__(self, context):
        self.context = context

    def do_foo(self):
        BarManager.any(self.context).do_bar()


@interface
class BarManager(object):
    def __init__(self, context):
        pass


# @components implement @interfaces

@component(BarManager)
class DebianBarManager(BarManager):
    def __init__(self, context):
        pass

    @classmethod
    def __verify__(cls):
        return os.path.exists('/etc/debian_version')

    def do_bar(self):
        subprocess.call(['cowsay', 'bar'])


@component(BarManager)
class RHELBarManager(BarManager):
    def __init__(self, context):
        pass

    @classmethod
    def __verify__(cls):
        return os.path.exists('/etc/redhat-release')

    def do_bar(self):
        subprocess.call(['yum', 'install', 'bar'])


# Context tracks instantiated @services and @components
ctx = Context()

assert FooService.get(ctx) == FooService.get(ctx)

# .all() returns instance of each implementation
assert len(BarManager.all(ctx)) == 2

# .classes() returns class of each implementation
assert len(BarManager.classes(ctx)) == 2

# .any() returns first available implementation
assert isinstance(BarManager.any(ctx), BarManager)

foo = FooService.get(ctx)
foo.do_foo()

```
