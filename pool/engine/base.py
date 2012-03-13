#!/usr/local/bin/python2.7
#coding:utf-8

class Connectable(object):
    """Interface for an object which supports execution of SQL constructs.

    The two implementations of :class:`.Connectable` are :class:`.Connection` and
    :class:`.Engine`.

    Connectable must also implement the 'dialect' member which references a
    :class:`.Dialect` instance.

    """

    def connect(self, **kwargs):
        """Return a :class:`.Connection` object.
        Depending on context, this may be ``self`` if this object
        is already an instance of :class:`.Connection`, or a newly 
        procured :class:`.Connection` if this object is an instance
        of :class:`.Engine`.
        """

    def contextual_connect(self):
        """Return a :class:`.Connection` object which may be part of an ongoing
        context.

        Depending on context, this may be ``self`` if this object
        is already an instance of :class:`.Connection`, or a newly 
        procured :class:`.Connection` if this object is an instance
        of :class:`.Engine`.
        """

        raise NotImplementedError()

    def create(self, entity, **kwargs):
        """Emit CREATE statements for the given schema entity."""

        raise NotImplementedError()

    def drop(self, entity, **kwargs):
        """Emit DROP statements for the given schema entity."""

        raise NotImplementedError()

    def execute(self, object, *multiparams, **params):
        """Executes the given construct and returns a :class:`.ResultProxy`."""
        raise NotImplementedError()

    def scalar(self, object, *multiparams, **params):
        """Executes and returns the first column of the first row.

        The underlying cursor is closed after execution.
        """
        raise NotImplementedError()

    def _run_visitor(self, visitorcallable, element, 
                                    **kwargs):
        raise NotImplementedError()

    def _execute_clauseelement(self, elem, multiparams=None, params=None):
        raise NotImplementedError()

