"""Image Library Functions"""

import os

BIN_EXTS = ['.bin', '.raw', '.dat', '.binp']


__all__ = list(globals())


def imcvt(img, size=None, color=None):
    import cv2
    img = img if not size else cv2.resize(img, (size[0] if size[0] > 0 else img.shape[1], size[1] if size[1] > 0 else img.shape[0]))
    img = img if not color else cv2.cvtColor(img, getattr(cv2, 'COLOR_' + color.upper()))
    return img


def imread(path, size=None, color=None):
    import os, cv2, numpy
    ext = os.path.splitext(path)[1].lower()
    data = numpy.fromfile(path, numpy.uint8)
    img = cv2.imdecode(data, -1) if ext not in BIN_EXTS else data
    assert img is not None, 'File is not a image: "%s"' % path
    img = imcvt(img, size, color)
    return img


def imwrite(path, img, size=None, color=None):
    import os, cv2
    img = imcvt(img, size, color)
    folder = os.path.dirname(path)
    folder and os.makedirs(folder, exist_ok=True)
    ext = os.path.splitext(path)[1].lower()
    data = cv2.imencode(ext, img)[1] if ext not in BIN_EXTS else img
    data.tofile(path)


def imshow(img, delay=50, title='', size=None, color=None):  # for test
    import cv2
    img = imcvt(img, size, color)
    cv2.imshow('', img)
    try:
        title2 = title.encode('gbk').decode()
        cv2.setWindowTitle('', title2)
    except UnicodeError:
        try:
            import win32gui
            cv2.setWindowTitle('', 'IMTITLE')
            hwnd = win32gui.FindWindow(0, 'IMTITLE')
            win32gui.SetWindowText(hwnd, title)
        except Exception:
            cv2.setWindowTitle('', title)
    cv2.waitKey(delay)


def imsave(path, start=0, step=1, stop=float('inf')):  # for test
    folder = os.path.splitext(path)[0]
    for n, img in enumerate(imiter(path)):
        if n >= stop:
            return
        if n >= start and (n - start) % step == 0:
            imwrite('%s/img_%05d.png' % (folder, n), img)


def imiter(file_or_id):
    import cv2
    cap = cv2.VideoCapture(file_or_id)
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            cap.release()
            return
        yield img


__all__ = [k for k in globals() if k not in __all__]
