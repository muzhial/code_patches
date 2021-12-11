import numpy as np
import cv2


src_path = '/home/gdd/Desktop/2007_001526.jpg'

src_img = cv2.imread(src_path)
height, width = src_img.shape[:2]

src_pt = np.array([[50, 50],
                   [50, 250],
                   [250, 50]], dtype=np.float32)

dst_pt = np.array([[250, 50],
                   [50, 50],
                   [250, 250]], dtype=np.float32)

trans = cv2.getAffineTransform(np.float32(src_pt), np.float32(dst_pt))

print(trans)

pt = np.array([0, 0, 1])
print(trans @ pt)

img = cv2.warpAffine(
    src_img,
    trans, (width, height),
    flags=cv2.INTER_LINEAR)

cv2.imwrite('./test.png', img)
