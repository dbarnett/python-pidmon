import logging
import os
import multiprocessing
import time

import pidmon

logger = logging.getLogger(__name__)

def _run_DummyProcess(q):
    q.get()     # die as soon as something is put on queue

class DummyProcess(object):
    """Throw-away process to wait idle until stopped"""
    def __init__(self, queue=None, target=_run_DummyProcess, args=None):
        if queue is None:
            queue = multiprocessing.Queue()
        if args is None:
            args = (queue,)
        self.queue = queue
        self.process = multiprocessing.Process(target=target, args=args)

    def start(self):
        self.process.start()

    def stop(self):
        if self.process.is_alive():
            self.queue.put('STOP')
            self.process.join()

def _run_SpawnOnceProcess(q):
    p = DummyProcess(q)
    p.start()
    logger.info("Started child, PID {}".format(p.process.pid))
    p.process.join()
    logger.info("Child {} finished".format(p.process.pid))

class SpawnOnceProcess(DummyProcess):
    def __init__(self):
        DummyProcess.__init__(self, target=_run_SpawnOnceProcess)

