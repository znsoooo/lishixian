import wx

__all__ = list(globals())


def center(top):
    '''tkinter set center'''
    top.update_idletasks()
    x = (top.winfo_screenwidth()  - top.winfo_reqwidth())  / 2
    y = (top.winfo_screenheight() - top.winfo_reqheight()) / 2
    top.geometry('+%d+%d'%(x, y))


# todo staticbox = ?

class Mover:
    def __init__(self, parent, widget):
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


__all__ = [k for k in globals() if k not in __all__]
