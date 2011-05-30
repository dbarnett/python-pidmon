import os
import unittest
import threading
import time

import pidmon
from ._utils import DummyProcess

class TestProcessObj(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equal(self):
        self.assertEqual(pidmon.Process(1), pidmon.Process(1))

class TestListProcesses(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_self_in_processes(self):
        """list_processes() should contain current python process's PID"""
        running_pids = [p.pid for p in pidmon.list_processes()]
        assert (os.getpid() in running_pids)

    def test_child_in_processes(self):
        """list_processes() should contain new process's PID"""
        running_pids_pre = [p.pid for p in pidmon.list_processes()]
        p1 = DummyProcess()
        try:
            p1.start()
            while p1.process.pid is None:        # make sure it's started
                pass
            assert (p1.process.pid not in running_pids_pre)
            running_pids = [p.pid for p in pidmon.list_processes()]
            assert (p1.process.pid in running_pids), "{} not in {!r}".format(p1.process.pid, running_pids)
        finally:
            p1.stop()
        running_pids_post = [p.pid for p in pidmon.list_processes()]
        assert (p1.process.pid not in running_pids_post)

class TestWaitPID(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def _stop_process_after(p, delay):
        def _sleep_n_stop(p, delay):
            time.sleep(delay)
            p.stop()
        t = threading.Thread(target=_sleep_n_stop, args=(p, delay))
        t.setDaemon(True)
        t.start()

    @staticmethod
    def _unused_pid():
        running_pids = [p.pid for p in pidmon.list_processes()]
        i = 1
        while i in running_pids:
            i += 1
        return i

    def test_unused_pid(self):
        """Waiting on an unused PID should return immediately"""
        unused_pid = self._unused_pid()
        t0 = time.time()
        pidmon.waitpid(unused_pid)
        t1 = time.time()
        time_taken = t1 - t0
        self.assertLess(time_taken, .5)

    def test_childpid(self, delay=.05):
        """Handles direct child (nothing os.waitpid can't do)"""
        p1 = DummyProcess()
        try:
            p1.start()
            self._stop_process_after(p1, delay)
            t0 = time.time()
            pidmon.waitpid(p1.process.pid)
        finally:
            p1.stop()
        t1 = time.time()
        assert (delay < t1 - t0), "died {:.2f}s into {:.2f}s delay".format(t1 - t0, delay)
