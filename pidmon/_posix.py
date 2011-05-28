import re
import subprocess

def ps(args):
    p = subprocess.Popen(['ps']+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.wait() == 0:
        for line in p.stdout.read().splitlines()[1:]:
            m = re.match(r'\s*(\d+) ', line)
            if m:
                yield int(m.group(1))

def list_processes():
    return list(ps(['-e']))

def get_children(pid):
    return list(ps(['--ppid', str(pid)]))

