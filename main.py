import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]]

finalText = ""

keyboard = Controller()

#全てを呼び出す
def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), t=8, colorC=(0,255,127), rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 144, 30), cv2.FILLED)
        cv2.putText(img, button.text, (x + 13, y + 70),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    return img

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([110 * j + 50, 110 * i + 50], key))
        # buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawALL(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x-10,y-10), (x + w+5, y + h+5), (205, 0, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 13, y + 70),
                            cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)
                #when clicked
                if l < 50:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 154), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 13, y + 70),
                                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                    finalText += button.text
                    sleep(0.8)

    cv2.rectangle(img, (50,600), (1000,500), (222, 196, 176), cv2.FILLED)
    cv2.putText(img, finalText, (60, 590),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()