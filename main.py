import cvzone
import cv2
import mediapipe
import numpy
from cvzone.PoseModule import PoseDetector
import pprint
import os

SHIRTFOLDERPATH = "Resources/Shirts"
FIXEDRATION = 262/190
SHIRTRATIOHEIGHTWIDTH = 581/440

# cap = cv2.VideoCapture("Resources/Videos/1.mp4")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
detector = PoseDetector()


listShirts = os.listdir(SHIRTFOLDERPATH)

imgnumber = 0
counterRight = 0
counterLeft = 0
imgButtonRight = cv2.imread("Resources/Button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
while True:
    _, img = cap.read()
    img = detector.findPose(img, draw = False)
    lmList, bboxInfo = detector.findPosition(img,
                                             bboxWithHands=False,
                                             draw = False)
    if lmList:
        lm11 = lmList[11][0:2] #get (x, y)
        lm12 = lmList[12][0:2] #get (x, y)

        imgShirt = cv2.imread(os.path.join(SHIRTFOLDERPATH, listShirts[imgnumber]),
                              cv2.IMREAD_UNCHANGED)
        widthofshirt = int((lm11[0] - lm12[0]) * FIXEDRATION)
        try:
            if widthofshirt < 100 and widthofshirt > 20:
                img = cv2.putText(img, "stand up straight", (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
            imgShirt = cv2.resize(imgShirt, (widthofshirt, int(widthofshirt*SHIRTRATIOHEIGHTWIDTH)))

            currentScale = int(lm11[0] - lm12[0]) / 190
            offset = int(44 * currentScale), int(48 * currentScale)

            img = cvzone.overlayPNG(img, imgShirt, (lm12[0]-offset[0], lm12[1]-offset[1]))
            img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
            img = cvzone.overlayPNG(img, imgButtonLeft,  (72  , 293))

            if lmList[16][0] < 150:
                counterLeft += 1
                cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                            counterLeft * 10, (0, 255, 0), 20)
                if counterLeft * 10 > 360:
                    counterLeft = 0
                    if imgnumber == 0:
                        imgnumber = len(listShirts) - 1
                    else:
                        imgnumber -= 1
            elif lmList[15][0] > 1100:
                counterRight += 1
                cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                            counterRight * 10, (0, 255, 0), 20)
                if counterRight * 10 > 360:
                    counterRight = 0
                    if imgnumber == len(listShirts) - 1:
                        imgnumber = 0
                    else:
                        imgnumber += 1
            else:
                counterLeft = 0
                counterRight = 0
        except:
            img = cv2.putText(img, "Turn Around", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)