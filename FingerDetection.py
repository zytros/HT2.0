import math

import HTMod as htm
import cv2
import numpy as np
import time


def between(x, a, b):
    return a < x < b


def distance(x1, y1, x2, y2):
    x = abs(x1 - x2)
    y = abs(y1 - y2)
    return math.sqrt(x * x + y * y)
    #return math.dist((x1, y1), (x2, y2))



detector = htm.handDetector(detectionCon = 0.7)
cap = cv2.VideoCapture(0)
imgBlackSrc = np.zeros((400, 800, 3), np.uint8)
imgBlack = imgBlackSrc.copy()
startTime = time.time()
curTime = 0
maxDist = 1
angle = 0
while True:
    success, img = cap.read()
    #img = cv2.flip(img, 1)
    h, w, c = img.shape
    center = (int(w/2), int(h/2))
    cv2.circle(img, center, 10, (255, 255, 255, cv2.FILLED))
    curTime = time.time() - startTime
    img = detector.findHands(img, True)
    #cv2.putText(imgBlack, str(curTime), (0, 25), cv2.FONT_ITALIC, 1, (255, 0, 0), 1)
    lmlist = detector.findPositions(img, 0, False)

    if len(lmlist) != 0:
        x1 = lmlist[5][1]
        y1 = lmlist[5][2]
        x2 = lmlist[8][1]
        y2 = lmlist[8][2]

        dist = distance(x1, y1, x2, y2)

        x = x2 - x1 #angle of finger
        y = y2 - y1
        angle = math.atan2(y, x)

        px = int((math.cos(angle) * (dist / maxDist * (h/2))) + w/2)
        py = int((math.sin(angle) * (dist / maxDist * (h/2))) + h/2)
        cv2.line(img, center, (px, py), (0, 255, 255), 4)

        #print(angle / math.pi * 180)
    if between(curTime, 10, 20):#mod1
        cv2.putText(imgBlack, "show full length", (0, 55), cv2.FONT_ITALIC, 1, (255, 255, 255), 1)
        if len(lmlist) != 0:

            length = distance(x1, y1, x2, y2)
            if length > maxDist:
                maxDist = length
        #print(maxDist)

    cv2.imshow("Helper", imgBlack)
    cv2.imshow("Image", img)
    imgBlack = imgBlackSrc.copy()
    cv2.waitKey(1)