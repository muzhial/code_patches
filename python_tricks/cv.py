import numpy as np
import cv2


def _get_3rd_point(a, b):
    assert len(a) == 2
    assert len(b) == 2
    direction = a - b
    third_pt = b + np.array([-direction[1], direction[0]], dtype=np.float32)

    return third_pt

src_path = './outputs/2007_001526.jpg'

src_img = cv2.imread(src_path)
height, width = src_img.shape[:2]

radius = 4
cv2.circle(src_img, (int(339), int(162)),
            radius, (int(255), int(0), int(0)), -1)
cv2.imwrite('./outputs/c_img.jpg', src_img)

src_pt = np.zeros((3, 2), dtype=np.float32)

scale = np.array([247.96825, 330.62433])
center = np.array([339.8183, 162.96982])
cen_2 = np.array([339.81829834, 38.98569489])
cen_3 = _get_3rd_point(center, cen_2)

# dst_pt = np.array([[250, 50],
#                    [50, 50],
#                    [250, 250]], dtype=np.float32)

# trans = cv2.getAffineTransform(np.float32(src_pt), np.float32(dst_pt))

# print(trans)

# pt = np.array([0, 0, 1])
# print(trans @ pt)

# img = cv2.warpAffine(
#     src_img,
#     trans, (1000, 1000),
#     flags=cv2.INTER_LINEAR)

# cv2.imwrite('./outputs/test2.png', img)
