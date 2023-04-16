from tkinter import *
import cv2

cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

while True:
    ret, frame0 = cap0.read()
    if ret:
        cv2.imshow("Frame 0", frame0)
    ret, frame1 = cap1.read()
    if ret:
        cv2.imshow("Frame 0", frame1)
    if cv2.waitKey(1) in [32, ]: break

cap0.release()
cap1.release()
cv2.destroyAllWindows()