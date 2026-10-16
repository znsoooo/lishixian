"""Office Automation"""

import os
import sys
import time
from threading import Thread


__all__ = list(globals())


def shortcut(to=None, create=True):  # get_path: desktop/programs/startup/...
    import winshell
    folder = to or winshell.desktop()
    target = sys.argv[0]
    name = os.path.splitext(os.path.basename(target))[0]
    path = os.path.join(folder, name + '.lnk')
    if create:
        winshell.CreateShortcut(path, target)
    elif os.path.exists(path):  # remove shortcut
        os.remove(path)


def paste(word, tab=0):
    import pyautogui
    import pyperclip
    for i in range(tab):
        pyautogui.press('tab')
    bak = pyperclip.paste()
    pyperclip.copy(word)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy(bak)


class Monitor:
    def __init__(self, func):
        import pynput
        self.pynput = pynput
        self.func = func
        Thread(target=self.mouser).start()
        Thread(target=self.keyboarder).start()

    def hook(self, *typ_names):
        for name in typ_names:
            yield (lambda typ: (lambda *args: self.func(typ, *args)))(name)

    def mouser(self):
        with self.pynput.mouse.Listener(*self.hook('move', 'click', 'scroll')) as self.ml:
            self.ml.join()

    def keyboarder(self):
        with self.pynput.keyboard.Listener(*self.hook('press', 'release')) as self.kl:
            self.kl.join()

    def stop(self):
        self.pynput.keyboard.Listener.stop(self.kl)
        self.pynput.mouse.Listener.stop(self.ml)


class Recoder:
    def __init__(self, complete=False):
        self.complete = complete

        self.clock = time.time()
        self.monitor = Monitor(self.callback)
        self.stop = self.monitor.stop

    def callback(self, typ, *args):
        if typ == 'move':
            if self.complete:
                x, y = args
                self.log('pyautogui.moveTo(%d, %d)' % (x, y))

        elif typ == 'click':
            x, y, button, pressed = args
            if self.complete:
                event = 'mouseDown' if pressed else 'mouseUp'
                self.log("pyautogui.%s(%d, %d, '%s')" % (event, x, y, button.name))
            elif pressed:
                self.log("pyautogui.click(%d, %d)" % (x, y))

        elif typ == 'scroll':
            x, y, dx, dy = args
            self.log('Scrolled {0}'.format((x, y))) # todo

        elif typ in ('press', 'release'):
            key, = args
            event = 'keyDown' if typ == 'press' else 'keyUp'
            self.log("pyautogui.%s(%s)" % (event, key))

    def log(self, msg):
        dt = time.time() - self.clock
        if self.complete:
            print('time.sleep(%.3f)' % dt)
            self.clock += dt
        elif dt > 0.5:
            dt = dt - dt % 0.5
            print('time.sleep(%.1f)' % dt)
            self.clock += dt
        print(msg)


__all__ = [k for k in globals() if k not in __all__]


if __name__ == '__main__':
    m = Recoder()
    # m = Recoder(complete=True)
    time.sleep(2)
    m.stop()


# todo 全局快捷键（组合键）
