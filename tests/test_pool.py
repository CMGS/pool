import time
import threading
from nose.tools import eq_
import pool.pool as M

def test_thread_safe_factory_should_not_interfered_between_threads():
    @M.ThreadSafeFactory
    class MemcacheClient(object):
        def get(self, key):
            self.to_return = key
            # time.sleep to make thread switch, like socket operations
            time.sleep(1)
            return self.to_return

    def run_in_thread(func, args=(), kwargs={}, return_holder=[]):
        def f():
            ret = func(*args, **kwargs)
            return_holder.append(ret)
        t = threading.Thread(target=f)
        t.start()
        return t

    mc = MemcacheClient()
    r1, r2 = [], []
    t1 = run_in_thread(mc.get, args=(1,), return_holder=r1)
    t2 = run_in_thread(mc.get, args=(2,), return_holder=r2)
    t1.join()
    t2.join()
    eq_(r1, [1])
    eq_(r2, [2])


