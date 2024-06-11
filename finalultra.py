import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 8
ECHO = 10

print("Distance measurement")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

print("Setting up sensor")
time.sleep(2)

def measure_distance():
    # Trigger the sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for the echo to start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for the echo to end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate the distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print("distance", distance)
    
    return distance

try:
    while True:
        distance = measure_distance()
        
        if distance <= 10:
            print("Stop")
        else:
            print("Go")
        
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    GPIO.cleanup()  # Reset GPIO settings
