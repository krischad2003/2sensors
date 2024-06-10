import RPi.GPIO as GPIO
import time
import smbus
# sudo apt-get install python3-rpi.gpio
# sudo apt-get install smbus
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

# Initialize I2C
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1 initialize the I2C 
ESP32_I2C_ADDRESS = 0x08  # ESP32 I2C address 

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

# function to send the command. 
def send_command(command):
    bus.write_byte(ESP32_I2C_ADDRESS, ord(command[0]))# sends the command at index 0 to the I2C address given. 

try:
    while True:
        distance = measure_distance()
        
        if distance <= 10:
            print("Stop")
            send_command("s")  # Send 's' for stop
        else:
            print("Go")
            send_command("g")  # Send 'g' for go
        
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    GPIO.cleanup()  # Reset GPIO settings
