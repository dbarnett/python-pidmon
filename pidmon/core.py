class ProcessBase(object):
    pid = None
    name = None
    command_line = None
    parent = None
    children = None
    user = None
    start_time = None

    def __init__(self, pid):
        self.pid = pid

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.pid)

    def __eq__(self, other):
        return self.pid == other.pid

    def get_descendants(self):
        last_procs = None
        procs = [self]
        while procs != last_procs:
            last_procs = procs
            for p in last_procs:
                for child_proc in p.children:
                    if child_proc not in procs:
                        procs.append(child_proc)

        return procs[1:]
