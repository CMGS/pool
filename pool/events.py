# sqlalchemy/events.py
# Copyright (C) 2005-2012 the SQLAlchemy authors and contributors <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Core event interfaces."""

from . import event, util
pool = util.importlater('pool', 'pool')

class PoolEvents(event.Events):
    """Available events for :class:`.Pool`.

    The methods here define the name of an event as well
    as the names of members that are passed to listener
    functions.

    e.g.::

        from sqlalchemy import event

        def my_on_checkout(dbapi_conn, connection_rec, connection_proxy):
            "handle an on checkout event"

        event.listen(Pool, 'checkout', my_on_checkout)

    In addition to accepting the :class:`.Pool` class and :class:`.Pool` instances,
    :class:`.PoolEvents` also accepts :class:`.Engine` objects and
    the :class:`.Engine` class as targets, which will be resolved
    to the ``.pool`` attribute of the given engine or the :class:`.Pool`
    class::

        engine = create_engine("postgresql://scott:tiger@localhost/test")

        # will associate with engine.pool
        event.listen(engine, 'checkout', my_on_checkout)

    """

    @classmethod
    def _accept_with(cls, target):
        if isinstance(target, type):
            if issubclass(target, pool.Pool):
                return target
        else:
            return target

    def connect(self, dbapi_connection, connection_record):
        """Called once for each new DB-API connection or Pool's ``creator()``.

        :param dbapi_con:
          A newly connected raw DB-API connection (not a SQLAlchemy
          ``Connection`` wrapper).

        :param con_record:
          The ``_ConnectionRecord`` that persistently manages the connection

        """

    def first_connect(self, dbapi_connection, connection_record):
        """Called exactly once for the first DB-API connection.

        :param dbapi_con:
          A newly connected raw DB-API connection (not a SQLAlchemy
          ``Connection`` wrapper).

        :param con_record:
          The ``_ConnectionRecord`` that persistently manages the connection

        """

    def checkout(self, dbapi_connection, connection_record, connection_proxy):
        """Called when a connection is retrieved from the Pool.

        :param dbapi_con:
          A raw DB-API connection

        :param con_record:
          The ``_ConnectionRecord`` that persistently manages the connection

        :param con_proxy:
          The ``_ConnectionFairy`` which manages the connection for the span of
          the current checkout.

        If you raise a :class:`~sqlalchemy.exc.DisconnectionError`, the current
        connection will be disposed and a fresh connection retrieved.
        Processing of all checkout listeners will abort and restart
        using the new connection.
        """

    def checkin(self, dbapi_connection, connection_record):
        """Called when a connection returns to the pool.

        Note that the connection may be closed, and may be None if the
        connection has been invalidated.  ``checkin`` will not be called
        for detached connections.  (They do not return to the pool.)

        :param dbapi_con:
          A raw DB-API connection

        :param con_record:
          The ``_ConnectionRecord`` that persistently manages the connection

        """

