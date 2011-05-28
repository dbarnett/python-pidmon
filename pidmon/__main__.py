import sys
from . import waitpid

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if argv[1] == 'waitpid':
        kw = {}
        if '-r' in argv:
            argv.remove('-r')
            kw['recursive'] = True
        pid = int(argv[2])
        waitpid(pid, **kw)

sys.exit(main())
