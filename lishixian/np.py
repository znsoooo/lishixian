import cv2
import numpy as np

__all__ = list(globals())


def imread(file):
    return cv2.imdecode(np.fromfile(file, np.uint8), -1)


def imwrite(file, im):
    cv2.imencode('.jpg', im)[1].tofile(file)


def imshow(img, title=''):  # for test
    cv2.namedWindow(title)
    cv2.imshow(title, img)
    cv2.waitKey(0)


def imiter(cap):
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            cap.release()
            break
        yield img

# cap = cv2.VideoCapture('VID_20191211_162134.mp4')
# for img in imiter(cap):
#     ...


__all__ = [k for k in globals() if k not in __all__]
