import re
import subprocess

from .core import ProcessBase

def ps(args):
    p = subprocess.Popen(['ps']+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.wait() == 0:
        for line in p.stdout.read().splitlines()[1:]:
            m = re.match(r'\s*(\d+) ', line)
            if m:
                yield int(m.group(1))

class PosixProcess(ProcessBase):
    def _get_value(self, valname):
        p = subprocess.Popen(['ps', '-p', str(self.pid), '-o', valname+'='], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.wait() == 0:
            return p.stdout.read().strip()
        return None

    @property
    def name(self):
        return self._get_value('comm')

    @property
    def command_line(self):
        return self._get_value('cmd')

    @property
    def parent(self):
        ppid_str = self._get_value('ppid')
        if ppid_str is not None:
            return PosixProcess(int(ppid_str))
        return None

    @property
    def children(self):
        return [PosixProcess(p) for p in ps(['--ppid', str(self.pid)])]

    @property
    def user(self):
        return self._get_value('user')

    @property
    def start_time(self):
        """Returns as string, probably should be date/datetime obj"""
        return self._get_value('time')

def list_processes():
    return [PosixProcess(p) for p in ps(['-e'])]

