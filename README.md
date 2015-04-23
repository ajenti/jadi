# Jadi

[![Build Status](https://travis-ci.org/ajenti/jadi.svg)](https://travis-ci.org/ajenti/jadi)

Minimalistic IoC for Python

```python
import os
import subprocess
from jadi import service, component, interface, Context


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



ctx = Context()

assert FooService.get(ctx) == FooService.get(ctx)

assert len(BarManager.all(ctx)) == 2
assert len(BarManager.classes(ctx)) == 2

assert isinstance(BarManager.any(ctx), BarManager)

foo = FooService.get(ctx)
foo.do_foo()

```
