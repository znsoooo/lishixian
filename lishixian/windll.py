"""Windows Dialog"""

import ctypes
from ctypes.wintypes import DWORD, WORD, LPARAM, LPVOID, HWND, HINSTANCE

LPOFNHOOKPROC = ctypes.c_void_p
LPCTSTR = LPTSTR = ctypes.c_wchar_p

OFN_ENABLESIZING    = 0x00800000
OFN_PATHMUSTEXIST   = 0x00000800
OFN_OVERWRITEPROMPT = 0x00000002
OFN_NOCHANGEDIR     = 0x00000008
MAX_PATH            = 1024

GetOpenFileName = ctypes.windll.comdlg32.GetOpenFileNameW
GetSaveFileName = ctypes.windll.comdlg32.GetSaveFileNameW


class OPENFILENAME(ctypes.Structure):
    _fields_ = [('lStructSize',       DWORD),
                ('hwndOwner',         HWND),
                ('hInstance',         HINSTANCE),
                ('lpstrFilter',       LPCTSTR),
                ('lpstrCustomFilter', LPTSTR),
                ('nMaxCustFilter',    DWORD),
                ('nFilterIndex',      DWORD),
                ('lpstrFile',         LPTSTR),
                ('nMaxFile',          DWORD),
                ('lpstrFileTitle',    LPTSTR),
                ('nMaxFileTitle',     DWORD),
                ('lpstrInitialDir',   LPCTSTR),
                ('lpstrTitle',        LPCTSTR),
                ('flags',             DWORD),
                ('nFileOffset',       WORD),
                ('nFileExtension',    WORD),
                ('lpstrDefExt',       LPCTSTR),
                ('lCustData',         LPARAM),
                ('lpfnHook',          LPOFNHOOKPROC),
                ('lpTemplateName',    LPCTSTR),
                ('pvReserved',        LPVOID),
                ('dwReserved',        DWORD),
                ('flagsEx',           DWORD)]


def BuildOFN(title, filter, buf):
    ofn = OPENFILENAME()
    ofn.lStructSize = ctypes.sizeof(OPENFILENAME)
    ofn.lpstrTitle = title
    ofn.lpstrFile = ctypes.cast(buf, LPTSTR)
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


__all__ = list(globals())


messagebox = lambda info, title='Message', style=0: ctypes.windll.user32.MessageBoxW(0, str(info), str(title), style)


def OpenFileDialog(title=None, filter='', path=''):
    return FileDialog(GetOpenFileName, title, filter, path)


def SaveFileDialog(title=None, filter='', path=''):
    return FileDialog(GetSaveFileName, title, filter, path)


__all__ = [k for k in globals() if k not in __all__]


if __name__ == '__main__':
    path = OpenFileDialog()
    print(path)
    path = SaveFileDialog()
    print(path)
