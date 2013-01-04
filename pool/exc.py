# sqlalchemy/exc.py
# Copyright (C) 2005-2012 the Pool authors and contributors <see AUTHORS file>
#
# This module is part of Pool and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Exceptions used with Pool.

The base exception class is :class:`.PoolError`.

"""

class PoolError(Exception):
    """Generic error class."""


class ArgumentError(PoolError):
    """Raised when an invalid or conflicting function argument is supplied.

    This error generally corresponds to construction time state errors.

    """


class CircularDependencyError(PoolError):
    """Raised by topological sorts when a circular dependency is detected.
    
    There are two scenarios where this error occurs:
    
    * In a Session flush operation, if two objects are mutually dependent
      on each other, they can not be inserted or deleted via INSERT or 
      DELETE statements alone; an UPDATE will be needed to post-associate
      or pre-deassociate one of the foreign key constrained values.
      The ``post_update`` flag described at :ref:`post_update` can resolve 
      this cycle.
    * In a :meth:`.MetaData.create_all`, :meth:`.MetaData.drop_all`,
      :attr:`.MetaData.sorted_tables` operation, two :class:`.ForeignKey`
      or :class:`.ForeignKeyConstraint` objects mutually refer to each
      other.  Apply the ``use_alter=True`` flag to one or both,
      see :ref:`use_alter`.
      
    """
    def __init__(self, message, cycles, edges, msg=None):
        if msg is None:
            message += " Cycles: %r all edges: %r" % (cycles, edges)
        else:
            message = msg
        PoolError.__init__(self, message)
        self.cycles = cycles
        self.edges = edges

    def __reduce__(self):
        return self.__class__, (None, self.cycles, 
                            self.edges, self.args[0])

class DisconnectionError(PoolError):
    """A disconnect is detected on a raw connection.

    This error is raised and consumed internally by a connection pool.  It can
    be raised by the :meth:`.PoolEvents.checkout` event 
    so that the host pool forces a retry; the exception will be caught
    three times in a row before the pool gives up and raises 
    :class:`~pool.exc.InvalidRequestError` regarding the connection attempt.

    """


class TimeoutError(PoolError):
    """Raised when a connection pool times out on getting a connection."""


class InvalidRequestError(PoolError):
    """Pool was asked to do something it can't do.

    This error generally corresponds to runtime state errors.

    """

class ResourceClosedError(InvalidRequestError):
    """An operation was requested from a connection, cursor, or other
    object that's in a closed state."""


class PoolDeprecationWarning(DeprecationWarning):
    """Issued once per usage of a deprecated API."""


class PoolPendingDeprecationWarning(PendingDeprecationWarning):
    """Issued once per usage of a deprecated API."""


class PoolWarning(RuntimeWarning):
    """Issued at runtime."""
