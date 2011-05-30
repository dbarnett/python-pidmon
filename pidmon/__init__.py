import logging
import os
import time
if os.name == 'nt':
    from ._nt import list_processes
    from ._nt import WinProcess as Process
else:
    from ._posix import list_processes
    from ._posix import PosixProcess as Process

logger = logging.getLogger(__name__)

def waitpid(pid, recursive=False, sleep_time=.1):
    proc = Process(pid)
    wait_pids = [pid]
    last_pids = []
    while True:
        running_pids = [p.pid for p in list_processes()]
        pids_closed = [p for p in wait_pids if p not in running_pids]
        wait_pids = [p for p in wait_pids if p in running_pids]
        for p in pids_closed:
            logger.info("PID closed: {}".format(p))
        if recursive:
            for child_p in proc.get_descendants():
                if child_p.pid not in wait_pids:
                    wait_pids.append(child_p.pid)
        new_wait_pids = [p for p in wait_pids if p not in last_pids]
        if len(wait_pids) == 0:
            break
        if len(new_wait_pids):
            logger.info("Waiting on PIDs: {!r}".format(wait_pids))
        elif len(pids_closed):
            logger.info("Still waiting on PIDs: {!r}".format(wait_pids))
        time.sleep(sleep_time)
        last_pids = wait_pids
