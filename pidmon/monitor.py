from . import list_processes

class PidActivity(object):
    """Lists of started and stopped processes during some time period"""
    started_procs = None
    stopped_procs = None

    def __init__(self, started_procs, stopped_procs):
        self.started_procs = started_procs
        self.stopped_procs = stopped_procs

class PidMonitor(object):
    """Polls for proc-started/proc-stopped events"""
    def __init__(self):
        self.running_procs = []

    def poll_procs(self):
        cur_procs = list_processes()
        started_procs = [p for p in cur_procs if p not in self.running_procs]
        stopped_procs = [p for p in self.running_procs if p not in cur_procs]
        self.running_procs = cur_procs
        return PidActivity(started_procs, stopped_procs)

