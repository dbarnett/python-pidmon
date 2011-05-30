import logging
import os
import time

if os.name == 'nt':
    from ._nt import list_processes
    from ._nt import WinProcess as Process
else:
    from ._posix import list_processes
    from ._posix import PosixProcess as Process
from .monitor import PidMonitor

logger = logging.getLogger(__name__)

def waitpid(pid, recursive=False, graft_func=None, sleep_time=.1):
    """Waits for a given PID to stop, then returns.

    The PID does not have to be a child of the current process.
    `recursive` indicates whether the function should consider orphaned
        children as an indication that the process is 'still running'.
    `graft_func` is a function that takes a `pidmon.Process` object and
        returns `True` if the given process should be considered as an
        indication that the process is 'still running'.

    Note that the algorithm relies on polling to detect subsidiary processes,
    so if `sleep_time` is longer than the lifespan of some processes, strange
    things could happen."""
    proc = Process(pid)
    wait_procs = []
    last_procs = []
    monitor = PidMonitor()
    activity = monitor.poll_procs()
    if proc in activity.started_procs:
        wait_procs.append(proc)
    while True:
        activity = monitor.poll_procs()
        stopped_wait_procs = []
        for p in activity.stopped_procs:
            if p in wait_procs:
                logger.info("PID stopped: {}".format(p))
                stopped_wait_procs.append(p)
                wait_procs.remove(p)
        new_wait_procs = []
        if activity.started_procs:
            descendants = (proc.get_descendants() if recursive else [])
            for p in activity.started_procs:
                if (p in descendants or 
                        graft_func is not None and graft_func(p)):
                    wait_procs.append(p)
                    new_wait_procs.append(p)
        if len(wait_procs) == 0:
            break
        if len(new_wait_procs):
            logger.info("Waiting on PIDs: {!r}".format(wait_procs))
        elif len(stopped_wait_procs):
            logger.info("Still waiting on PIDs: {!r}".format(wait_procs))
        time.sleep(sleep_time)
        last_procs = wait_procs
