import logging
import os
import time
if os.name == 'nt':
    from ._nt import list_processes, get_children
else:
    from ._posix import list_processes, get_children

logger = logging.getLogger(__name__)

def waitpid(pid, recursive=False, sleep_time=.1):
    wait_pids = [pid]
    last_pids = []
    while True:
        running_pids = list_processes()
        pids_closed = [p for p in wait_pids if p not in running_pids]
        wait_pids = [p for p in wait_pids if p in running_pids]
        for p in pids_closed:
            logger.info("PID closed: {}".format(p))
        if recursive:
            for child_p in get_pid_descendants(pid):
                if child_p not in wait_pids:
                    wait_pids.append(child_p)
        new_wait_pids = [p for p in wait_pids if p not in last_pids]
        if len(wait_pids) == 0:
            break
        if len(new_wait_pids):
            logger.info("Waiting on PIDs: {!r}".format(wait_pids))
        elif len(pids_closed):
            logger.info("Still waiting on PIDs: {!r}".format(wait_pids))
        time.sleep(sleep_time)
        last_pids = wait_pids

def get_pid_descendants(pid):
    last_pids = None
    pids = [pid]
    while pids != last_pids:
        last_pids = pids
        for p in last_pids:
            for child_pid in get_children(p):
                if child_pid not in pids:
                    pids.append(child_pid)

    return pids[1:]
