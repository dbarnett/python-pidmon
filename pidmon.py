import logging
import os
import re
import subprocess
import time
if os.name == 'nt':
    import win32com.client

logger = logging.getLogger(__name__)

def list_posix_processes(args):
    p = subprocess.Popen(['ps']+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.wait() == 0:
        for line in p.stdout.read().splitlines()[1:]:
            m = re.match(r'\s*(\d+) ', line)
            if m:
                yield int(m.group(1))

def get_children(pid):
    if os.name == 'nt':
        WMI = win32com.client.GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        children = [p.Properties_('ProcessID').Value for p in processes if p.Properties_('ParentProcessId').Value == pid]
    elif os.name == 'posix':
        p = subprocess.Popen(['ps', '--ppid', str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        children = list(list_posix_processes(['--ppid', str(pid)]))
    return children

def list_processes():
    if os.name == 'nt':
        WMI = win32com.client.GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        return [p.Properties_('ProcessID').Value for p in processes]
    elif os.name == 'posix':
        return list(list_posix_processes(['-e']))

def pid_running(pid):
    if os.name == 'nt':
        WMI = win32com.client.GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        return any(p.Properties_('ProcessID').Value == pid for p in processes)
    elif os.name == 'posix':
        p = subprocess.Popen(['ps', '-p', str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return (p.wait() == 0)

def wait_for_pid(pid, sleep_time=.1):
    while True:
        if not pid_running(pid):
            break
        time.sleep(sleep_time)

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

def wait_pid_and_children(pid, sleep_time=.1):
    pids = [pid] + get_pid_descendants(pid)
    while True:
        if len(pids) == 0:
            break
        logger.debug("Waiting on {!r}".format(pids))
        for child_p in get_pid_descendants(pid):
            if child_p not in pids:
                pids.append(child_p)
        last_pids = pids
        pids = [p for p in pids if pid_running(p)]
        pids_closed = [p for p in last_pids if p not in pids]
        if len(pids_closed):
            logger.info("PIDs closed: {!r}".format(pids_closed))
        time.sleep(sleep_time)
