import cv2
import numpy as np


cap = cv2.VideoCapture(0)

# Define the desired window size
desired_width = 1280
desired_height = 720

pts = []
while 1:
    # Take each frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, (desired_width, desired_height))  # Resize the frame

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 0, 255])
    upper_red = np.array([255, 255, 255])

    if "mask" not in locals():
        mask = cv2.inRange(hsv, lower_red, upper_red)
    else:
        mask = mask | cv2.inRange(hsv, lower_red, upper_red)

    # Apply morphological operations to smooth and fine-tune the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)

    # Define the color for the overlay (BGR format)
    # color = (105, 105, 105)  # Red in this example

    print(frame.shape)
    zero_array = np.zeros_like(frame)
    print(zero_array[:, :, 2])
    zero_array[:, :, 2] = mask
    # Blend the image and the overlay using the mask
    blended = cv2.addWeighted(frame, 0.5, zero_array, 1, 0)
    cv2.imshow("Track Laser", blended)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
