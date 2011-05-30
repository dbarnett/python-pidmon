import win32com.client

from .core import ProcessBase

class WinProcess(ProcessBase):
    """Handle to a process running on MS Windows

    Looks up attributes using win32com.
    See http://msdn.microsoft.com/en-us/library/aa394372.aspx for details."""
    def _get_value(self, valname):
        WMI = win32com.client.GetObject('winmgmts:')
        for p in WMI.InstancesOf('Win32_Process'):
            if p.Properties_('ProcessID').Value == self.pid:
                return p.Properties_(valname).Value
        return None

    @property
    def name(self):
        return self._get_value('Name')

    @property
    def command_line(self):
        return self._get_value('CommandLine')

    @property
    def parent(self):
        ppid = self._get_value('ParentProcessId')
        if ppid is not None:
            return WinProcess(ppid)
        return None

    @property
    def children(self):
        return [p for p in list_processes() if p.parent.pid == self.pid]

    @property
    def start_time(self):
        """Returns, e.g., '20110530102249.403200-420'"""
        return self._get_value('CreationDate')

def list_processes():
    WMI = win32com.client.GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    return [WinProcess(p.Properties_('ProcessID').Value) for p in processes]

