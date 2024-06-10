import cv2
import numpy as np
# to run this: python3 -m venv nameofenv
# source venvnameyoumade/bin/activate
# make sure to go into environemnt before you install 
# should be pip3 install opencv-python
# pip3 install numpy

# Initialize the camera, adjust to select the correct camera. 
# this is the final form for the line follow
import smbus

# Initialize the I2C bus
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1
ESP32_I2C_ADDRESS = 0x08  # ESP32 I2C address
cap = cv2.VideoCapture(0)
cap.set(3, 160)  # Set width
cap.set(4, 120)  # Set height
def send_command(command):
    # Send a single character command to the ESP32
    bus.write_byte(ESP32_I2C_ADDRESS, ord(command[0]))

if not cap.isOpened():
    print("Error: Could not open camera.")
    cap.release()
else:
    print("Camera opened successfully.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Define color range for mask (adjust as needed)
    low_b = np.array([0, 0, 0])
    high_b = np.array([5, 5, 5])

    # Create mask
    mask = cv2.inRange(frame, low_b, high_b)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            print("CX:", cx, "CY:", cy)

            # Determine direction based on the position of the centroid
            if cx >= 120:
                print("Turn Left")
                send_command("l")  # Send 'l' for left
            elif cx <= 40:
                print("Turn Right")
                send_command("r")  # Send 'l' for left
            else:
                print("On Track")
                send_command("o")  # Send 'l' for left

            # Draw the center of the contour
            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
        else:
            print("No moments found")

        # Draw contours on the frame
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
    else:
        print("No contours found")

    # Display the mask and frame
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
