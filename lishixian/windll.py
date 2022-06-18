"""Windows Dialog"""

import ctypes
from ctypes.wintypes import DWORD, WORD, LPARAM, LPVOID, HWND, HINSTANCE

__all__ = ['MessageBox', 'DirDialog', 'OpenFileDialog', 'SaveFileDialog']

MessageBox = lambda info, title='Message', style=0: ctypes.windll.user32.MessageBoxW(0, str(info), str(title), style)


LPOFNHOOKPROC = ctypes.c_void_p
LPCSTR = LPSTR = ctypes.c_wchar_p

OFN_ENABLESIZING    = 0x00800000
OFN_PATHMUSTEXIST   = 0x00000800
OFN_OVERWRITEPROMPT = 0x00000002
OFN_NOCHANGEDIR     = 0x00000008
MAX_PATH            = 1024

GetOpenFileName = ctypes.windll.comdlg32.GetOpenFileNameW
GetSaveFileName = ctypes.windll.comdlg32.GetSaveFileNameW


# Ref: https://gist.github.com/nicomgd/1097a0b7ca3715da4e71

class OPENFILENAME(ctypes.Structure):
    _fields_ = [
        ('lStructSize',       DWORD),
        ('hwndOwner',         HWND),
        ('hInstance',         HINSTANCE),
        ('lpstrFilter',       LPCSTR),
        ('lpstrCustomFilter', LPSTR),
        ('nMaxCustFilter',    DWORD),
        ('nFilterIndex',      DWORD),
        ('lpstrFile',         LPSTR),
        ('nMaxFile',          DWORD),
        ('lpstrFileTitle',    LPSTR),
        ('nMaxFileTitle',     DWORD),
        ('lpstrInitialDir',   LPCSTR),
        ('lpstrTitle',        LPCSTR),
        ('Flags',             DWORD),
        ('nFileOffset',       WORD),
        ('nFileExtension',    WORD),
        ('lpstrDefExt',       LPCSTR),
        ('lCustData',         LPARAM),
        ('lpfnHook',          LPOFNHOOKPROC),
        ('lpTemplateName',    LPCSTR),
        ('pvReserved',        LPVOID),
        ('dwReserved',        DWORD),
        ('FlagsEx',           DWORD)
    ]


def BuildOFN(title, filter, buf):
    ofn = OPENFILENAME()
    ofn.lStructSize = ctypes.sizeof(OPENFILENAME)
    ofn.lpstrTitle = title
    ofn.lpstrFile = ctypes.cast(buf, LPSTR)
    ofn.nMaxFile = MAX_PATH
    ofn.lpstrFilter = filter # 'All types (*.*)\0*.*\0'
    ofn.Flags = OFN_ENABLESIZING | OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT | OFN_NOCHANGEDIR
    return ofn


def FileDialog(call, title, filter, path):
    filter = filter.replace('|', '\0')
    if filter and not filter.endswith('\0'):
        filter += '\0'
    buf = ctypes.create_unicode_buffer(path, MAX_PATH)
    ofn = BuildOFN(title, filter, buf)
    if call(ctypes.byref(ofn)):
        return buf[:].split('\0', 1)[0]


def OpenFileDialog(title=None, filter='', path=''):
    return FileDialog(GetOpenFileName, title, filter, path)


def SaveFileDialog(title=None, filter='', path=''):
    return FileDialog(GetSaveFileName, title, filter, path)


ole32 = ctypes.windll.ole32
shell32 = ctypes.windll.shell32

BIF_EDITBOX        = 0x0010
BIF_NEWDIALOGSTYLE = 0x0040
BIF_USENEWUI       = 0x0050

LPCTSTR = LPTSTR = ctypes.c_char_p


# Ref: https://github.com/Nolanlemahn/ProjectExist/blob/master/game/EasyDialogsWin.py
# Ref: https://github.com/apprenticeharper/DeDRM_tools/blob/master/DeDRM_plugin/askfolder_ed.py

class BROWSEINFO(ctypes.Structure):
    _fields_ = [
        ('hwndOwner',      HWND),
        ('pidlRoot',       LPVOID),
        ('pszDisplayName', LPTSTR),
        ('lpszTitle',      LPCTSTR),
        ('ulFlags',        ctypes.c_uint),
        ('lpfn',           LPVOID),
        ('lParam',         LPARAM),
        ('iImage',         ctypes.c_int)
    ]


def DirDialog(message=None):
    bi = BROWSEINFO()
    bi.pszDisplayName = ctypes.c_char_p(b'\0' * MAX_PATH)
    if message:
        bi.lpszTitle = message.encode('gbk')
    bi.ulFlags = BIF_USENEWUI

    shell32.SHBrowseForFolder.restype = LPVOID
    pidl = LPVOID(shell32.SHBrowseForFolder(ctypes.byref(bi)))
    if pidl:
        path = ctypes.c_char_p(b'\0' * MAX_PATH)
        shell32.SHGetPathFromIDList(pidl, path)
        ole32.CoTaskMemFree(pidl)
        result = path.value.decode('gbk')
        return result


if __name__ == '__main__':
    path = DirDialog()
    MessageBox(path)
    path = OpenFileDialog()
    MessageBox(path)
    path = SaveFileDialog()
    MessageBox(path)
