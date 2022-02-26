"""GUI Functions"""

from threading import Thread


__all__ = list(globals())


def center(top):
    """tkinter set center"""
    top.update_idletasks()
    x = (top.winfo_screenwidth()  - top.winfo_reqwidth())  / 2
    y = (top.winfo_screenheight() - top.winfo_reqheight()) / 2
    top.geometry('+%d+%d'%(x, y))


def WrapBox(parent, w, label=''):
    import wx
    box = wx.StaticBoxSizer(wx.VERTICAL, parent, label)
    box.Add(w)
    return box


def GetClipboard():
    import wx
    do = wx.TextDataObject()
    if wx.TheClipboard.Open():
        ret = wx.TheClipboard.GetData(do)
        wx.TheClipboard.Close()
        if ret:
            return do.GetText()


def SetClipboard(text):
    import wx
    do = wx.TextDataObject()
    do.SetText(text)
    if wx.TheClipboard.Open():
        wx.TheClipboard.SetData(do)
        wx.TheClipboard.Close()


class Mover:
    def __init__(self, parent, widget):
        import wx
        self.p = parent
        self.dxy = (0, 0)
        widget.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        parent.Bind(wx.EVT_LEFT_UP,   self.OnLeftUp)
        parent.Bind(wx.EVT_MOTION,    self.OnMouseMove)

    def OnLeftDown(self, evt):
        self.p.CaptureMouse()
        x, y = self.p.ClientToScreen(evt.GetPosition())
        x0, y0 = self.p.GetPosition()
        dx = x - x0
        dy = y - y0
        self.dxy = (dx, dy)

    def OnLeftUp(self, evt):
        if self.p.HasCapture():
            self.p.ReleaseMouse()

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.p.ClientToScreen(evt.GetPosition())
            fp = (x - self.dxy[0], y - self.dxy[1])
            self.p.Move(fp)


class EventThread(Thread):
    """
    Usage:
    widget.Bind(wx.PyEventBinder(id), lambda e: print(e.data))
    EventThread(widget, id, int, 7)
    """

    def __init__(self, parent, id, target=bool, *args, **kwargs):
        Thread.__init__(self, target=target, args=args, kwargs=kwargs)
        self.parent = parent
        self.id = id
        self.start()

    def run(self):
        import wx
        event = wx.PyEvent(0, self.id)
        event.data = self._target(*self._args, **self._kwargs)
        wx.PostEvent(self.parent, event)


__all__ = [k for k in globals() if k not in __all__]
