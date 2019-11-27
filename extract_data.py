import numpy as np
from PIL import ImageGrab
import cv2
import time


def screen_record():
    last_time = time.time()
    while True:
        # 800x600 windowed mode
        time.sleep(0.5)
        printscreen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 940)))
        cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


# waldo = cv2.imread('waldo.jpg')
# w = cv2.imread('iris.jpg')
# wshape = waldo.shape
# wshape2 = w.shape
# scene = cv2.imread('whereswaldo.jpg')
# res = cv2.matchTemplate(scene, waldo, cv2.TM_CCOEFF_NORMED)
# res2 = cv2.matchTemplate(scene, w, cv2.TM_CCOEFF_NORMED)
# minmax = cv2.minMaxLoc(res)
# minmax2 = cv2.minMaxLoc(res2)
#
# min_val, max_val, min_loc, max_loc = minmax
# _, max_val2, _, max_loc2 = minmax2
# corner1 = max_loc
# corner2 = (max_loc[0] + wshape[1], max_loc[1] + wshape[0] )
# corner1_ = max_loc2
# corner2_ = (max_loc2[0] + wshape2[1], max_loc2[1] + wshape2[0] )
# cv2.rectangle(scene, corner1, corner2, (255, 0, 0), 3)
# cv2.rectangle(scene, corner1_, corner2_, (255, 0, 0), 3)
# cv2.imshow("output", scene)
# cv2.waitKey(0)


if __name__ == '__main__':
    screen_record()




