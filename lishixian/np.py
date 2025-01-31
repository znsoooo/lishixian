"""Image Library Functions"""

import os


__all__ = list(globals())


def imread(path):
    import os, cv2, numpy
    ext = os.path.splitext(path)[1].lower()
    data = numpy.fromfile(path, numpy.uint8)
    img = cv2.imdecode(data, -1) if ext != '.bin' else data
    assert img is not None, 'File is not a image: "%s"' % path
    return img


def imwrite(path, img):
    import os, cv2
    folder = os.path.dirname(path)
    folder and os.makedirs(folder, exist_ok=True)
    ext = os.path.splitext(path)[1].lower()
    data = cv2.imencode(ext, img)[1] if ext != '.bin' else img
    data.tofile(path)


def imshow(img, delay=50, title=''):  # for test
    import cv2
    cv2.imshow('', img)
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
