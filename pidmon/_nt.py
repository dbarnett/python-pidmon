import win32com.client

def list_processes():
    WMI = win32com.client.GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    return [p.Properties_('ProcessID').Value for p in processes]

def get_children(pid):
    WMI = win32com.client.GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    return [p.Properties_('ProcessID').Value for p in processes if p.Properties_('ParentProcessId').Value == pid]
