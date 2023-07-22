"""Regedit"""

import winreg


__all__ = list(globals())


def GetDir(name, local=False): # Name: 'Desktop', 'SendTo', 'Programs', 'Startup'
    path = r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    if local:
        name = 'Common ' + name
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    else:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
    return winreg.QueryValueEx(key, name)[0]


def DeleteRecu(key):
    for i in range(winreg.QueryInfoKey(key)[0]):
        name = winreg.EnumKey(key, i)
        DeleteRecu(winreg.OpenKey(key, name))
        winreg.DeleteKey(key, name)


def DeleteKey(key, name=''):
    root, p = key.split('\\', 1)
    key2 = winreg.OpenKey(getattr(winreg, root), p)
    if name:
        winreg.DeleteValue(key2, name)
    else:
        DeleteRecu(key2)
        winreg.DeleteKey(getattr(winreg, root), p)


def SetKey(key, name='', val=''):
    root, p = key.split('\\', 1)
    key2 = winreg.CreateKey(getattr(winreg, root), p)
    winreg.SetValueEx(key2, name, 0, winreg.REG_SZ, val)


def NewFilePy():
    SetKey(r'HKEY_CURRENT_USER\Software\Classes\.py\ShellNew', 'FileName')


__all__ = [k for k in globals() if k not in __all__]
