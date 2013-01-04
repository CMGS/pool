#!/usr/local/bin/python2.7
#coding:utf-8

import re

class symbol(object):
    def __init__(self, name, doc=None):
        """Construct a new named symbol."""
        assert isinstance(name, str)
        self.name = name
        if doc:
            self.__doc__ = doc
    def __reduce__(self):
        return symbol, (self.name,)
    def __repr__(self):
        return "<symbol '%s>" % self.name

class memoized_property(object):
    """A read-only @property that is only evaluated once."""
    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result

_POOL_RE = re.compile(r'pool/([a-z_]+/){0,2}[a-z_]+\.py')
_UNITTEST_RE = re.compile(r'unit(?:2|test2?/)')
def chop_traceback(tb, exclude_prefix=_UNITTEST_RE, exclude_suffix=_POOL_RE):
    """Chop extraneous lines off beginning and end of a traceback.

    :param tb:
      a list of traceback lines as returned by ``traceback.format_stack()``

    :param exclude_prefix:
      a regular expression object matching lines to skip at beginning of ``tb``

    :param exclude_suffix:
      a regular expression object matching lines to skip at end of ``tb``
    """
    start = 0
    end = len(tb) - 1
    while start <= end and exclude_prefix.search(tb[start]):
        start += 1
    while start <= end and exclude_suffix.search(tb[end]):
        end -= 1
    return tb[start:end+1]

class importlater(object):
    """Deferred import object.

    e.g.::

        somesubmod = importlater("mypackage.somemodule", "somesubmod")

    is equivalent to::

        from mypackage.somemodule import somesubmod

    except evaluted upon attribute access to "somesubmod".

    importlater() currently requires that resolve_all() be
    called, typically at the bottom of a package's __init__.py.
    This is so that __import__ still called only at 
    module import time, and not potentially within
    a non-main thread later on.

    """

    _unresolved = set()

    def __init__(self, path, addtl=None):
        self._il_path = path
        self._il_addtl = addtl
        importlater._unresolved.add(self)

    @classmethod
    def resolve_all(cls):
        for m in list(importlater._unresolved):
            m._resolve()

    @property
    def _full_path(self):
        if self._il_addtl:
            return self._il_path + "." + self._il_addtl
        else:
            return self._il_path

    @memoized_property
    def module(self):
        if self in importlater._unresolved:
            raise ImportError(
                    "importlater.resolve_all() hasn't been called")

        m = self._initial_import
        if self._il_addtl:
            m = getattr(m, self._il_addtl)
        else:
            for token in self._il_path.split(".")[1:]:
                m = getattr(m, token)
        return m

    def _resolve(self):
        importlater._unresolved.discard(self)
        if self._il_addtl:
            self._initial_import = __import__(
                                self._il_path, globals(), locals(), 
                                [self._il_addtl])
        else:
            self._initial_import = __import__(self._il_path)

    def __getattr__(self, key):
        if key == 'module':
            raise ImportError("Could not resolve module %s" 
                                % self._full_path)
        try:
            attr = getattr(self.module, key)
        except AttributeError:
            raise AttributeError(
                        "Module %s has no attribute '%s'" %
                        (self._full_path, key)
                    )
        self.__dict__[key] = attr
        return attr

