"""Image Library Functions"""

import os


__all__ = list(globals())


def imread(file):
    import cv2
    import numpy as np
    return cv2.imdecode(np.fromfile(file, np.uint8), -1)


def imwrite(file, im):
    import cv2
    cv2.imencode('.jpg', im)[1].tofile(file)


def imshow(img, delay=50, title=''): # for test
    import cv2
    cv2.namedWindow(title)
    cv2.imshow(title, img)
    cv2.waitKey(delay)


def imsave(file): # for test
    import cv2
    folder = os.path.splitext(file)[0]
    os.makedirs(folder, exist_ok=True)
    for n, img in enumerate(imiter(file)):
        cv2.imwrite('%s/img_%04d.png' % (folder, n), img)


def imiter(file_or_id, st=None, ed=None):
    import cv2
    cap = cv2.VideoCapture(file_or_id)
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            cap.release()
            return
        yield img[st:ed]


# cap = cv2.VideoCapture('VID_20191211_162134.mp4')
# for img in imiter(cap):
#     ...


__all__ = [k for k in globals() if k not in __all__]
