import multiprocessing

def _run_DummyProcess(q):
    q.get()     # die as soon as something is put on queue

class DummyProcess(object):
    """Throw-away process to wait idle until stopped"""
    def __init__(self):
        self.queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=_run_DummyProcess, args=(self.queue,))

    def start(self):
        self.process.start()

    def stop(self):
        if self.process.is_alive():
            self.queue.put('STOP')
            self.process.join()
