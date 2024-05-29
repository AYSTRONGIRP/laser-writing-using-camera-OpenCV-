import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 1080)
pts = []
while 1:
    # Take each frame
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 0, 255])
    upper_red = np.array([255, 255, 255])

    if "mask" not in locals():
        mask = cv2.inRange(hsv, lower_red, upper_red)
    else:
        mask = mask | cv2.inRange(hsv, lower_red, upper_red)

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)

    cv2.circle(frame, maxLoc, 20, (0, 0, 255), 2, cv2.LINE_AA)

    # Define the color for the overlay (BGR format)
    # color = (210, 43, 43)  # Red in this example

    # Blend the image and the overlay using the mask
    blended = cv2.addWeighted(frame, 1, cv2.merge([mask, mask, mask]), 0.5, 0)
    cv2.imshow("Track Laser", blended)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()