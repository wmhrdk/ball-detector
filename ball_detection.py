#!/usr/bin/env python3

import cv2
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_normal = cv2.VideoWriter('output_normal.avi', fourcc, 24.0, (640, 480))
out_dilation = cv2.VideoWriter('output_dilation.avi', fourcc, 24.0, (640, 480))
out_res = cv2.VideoWriter('output_res.avi', fourcc, 24.0, (640, 480))

# Default color range variables
lowHue = 0; lowSat = 91; lowVal = 45
highHue = 37; highSat = 255; highVal = 255

def nothing(*arg):
        pass

# Create Trackbar
cv2.namedWindow('colorPick')
# Lower range colour sliders.
cv2.createTrackbar('lowHue', 'colorPick', lowHue, 255, nothing)
cv2.createTrackbar('lowSat', 'colorPick', lowSat, 255, nothing)
cv2.createTrackbar('lowVal', 'colorPick', lowVal, 255, nothing)
# Higher range colour sliders.
cv2.createTrackbar('highHue', 'colorPick', highHue, 255, nothing)
cv2.createTrackbar('highSat', 'colorPick', highSat, 255, nothing)
cv2.createTrackbar('highVal', 'colorPick', highVal, 255, nothing)

cap = cv2.VideoCapture(2)

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowHue = cv2.getTrackbarPos('lowHue', 'colorPick')
    lowSat = cv2.getTrackbarPos('lowSat', 'colorPick')
    lowVal = cv2.getTrackbarPos('lowVal', 'colorPick')
    highHue = cv2.getTrackbarPos('highHue', 'colorPick')
    highSat = cv2.getTrackbarPos('highSat', 'colorPick')
    highVal = cv2.getTrackbarPos('highVal', 'colorPick')

    lower_color = np.array([lowHue, lowSat, lowVal])
    upper_color = np.array([highHue, highSat, highVal])

    blurred = cv2.medianBlur(hsv, 5)

    mask = cv2.inRange(blurred, lower_color, upper_color)

    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=3)
    dilation = cv2.dilate(erosion, kernel, iterations=2)

    res = cv2.bitwise_and(frame, frame, mask=dilation)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, 600, param1=400, param2=30, minRadius=10, maxRadius=400)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(frame, (i[0], i[1]), i[2], (100,255,100),2)
            cv2.circle(frame, (i[0],i[1]), 2, (25,100,25), 3)
            xPos = i[0]
            yPos = i[1]
            ball_width = i[2] * 2
            zPos = (60 * 240) / ball_width
    else:
        xPos = 1
        yPos = 1
        zPos = 1
        ball_width = 1

    cv2.putText(frame, ('x='+str(int(xPos))), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,200,100), 2, cv2.LINE_AA)
    cv2.putText(frame, ('y='+str(int(yPos))), (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,200,100), 2, cv2.LINE_AA)

    fwidth = cap.get(3)
    fheight = cap.get(4)

    cv2.putText(frame, ('fw='+str(fwidth)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,250,250), 2, cv2.LINE_AA)
    cv2.putText(frame, ('fh='+str(fheight)), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,250,250), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('erosion', erosion)
    cv2.imshow('dilation', dilation)
    cv2.imshow('result', res)

    print("xPos = {} ||  ".format(xPos))
    print("yPos = {}\n".format(yPos))

    out_normal.write(frame)
    out_dilation.write(dilation)
    out_res.write(res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

xPos = 1
yPos = 1
zPos = 1
ball_width = 1

cap.release()
out_normal.release()
out_dilation.release()
out_res.release()
cv2.destroyAllWindows()
exit()
