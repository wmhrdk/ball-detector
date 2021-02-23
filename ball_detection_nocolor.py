import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, 600, param1=500, param2=500, minRadius=10, maxRadius=400)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(frame, (i[0],i[1]), i[2], (100,255,100),2)
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
    #cv2.putText(frame, ('z='+str(int(zPos))), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,200,100), 2, cv2.LINE_AA)

    fwidth = cap.get(3)
    fheight = cap.get(4)

    cv2.putText(frame, ('fw='+str(fwidth)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,250,250), 2, cv2.LINE_AA)
    cv2.putText(frame, ('fh='+str(fheight)), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,250,250), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

xPos = 1
yPos = 1
zPos = 1
ball_width = 1

cap.release()
cv2.destroyAllWindows()
exit()
