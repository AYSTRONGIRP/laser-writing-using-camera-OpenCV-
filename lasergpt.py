import cv2
import numpy as np

# Initialize video capture from the default camera (0)
cap = cv2.VideoCapture(0)

# Create an empty canvas (white image)
canvas = np.ones((480, 640, 3), dtype=np.uint8) * 255

# Initialize variables for drawing
drawing = False
prev_point = None

while True:
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define a range of red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Create a mask for the red color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 10:
            # Get the centroid of the contour
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                # Draw a circle at the centroid of the red laser pointer
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

                if drawing:
                    # If drawing is enabled, draw a line from the previous point to the current point
                    if prev_point is not None:
                        cv2.line(canvas, prev_point, (cx, cy), (0, 0, 0), 2)

                    prev_point = (cx, cy)
                else:
                    prev_point = None

    # Show the frames (frame with laser pointer detection and canvas)
    cv2.imshow("Frame", frame)
    cv2.imshow("Canvas", canvas)

    # Handle key events
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("d"):
        # Toggle drawing mode on/off
        drawing = not drawing

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
