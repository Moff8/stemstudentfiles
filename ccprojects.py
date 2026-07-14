'''
#LED control
from gpiozero import LED
import time

led = LED(26)
led.on()

time.sleep(5)

led.blink(on_time=1, off_time=1)

time.sleep(10)

led.off()




# Traffic Lights
from gpiozero import LED
from time import sleep

# Define the LEDs connected to GPIO pins
red = LED(13)
amber = LED(19)
green = LED(26)

try:
    while True:
        # Red light on for 5 seconds
        red.on()
        amber.off()
        green.off()
        sleep(5)

        # Red and amber lights on for 2 seconds
        amber.on()
        sleep(2)

        # Amber light on for 1 second
        red.off()
        sleep(1)

        # Green light on for 6 seconds
        amber.off()
        green.on()
        sleep(6)

        # Amber light on for 1 second
        green.off()
        amber.on()
        sleep(1)

except KeyboardInterrupt:
    # Turn off all LEDs when the program is stopped
    red.off()
    amber.off()
    green.off()
    
    
    

#Test the button and LED
from gpiozero import Button, LED
import time


button = Button(6)
button.wait_for_press()

print("The button was pressed!")

led = LED(26)
led.on()
time.sleep(10)
led.off()




#morse code
from gpiozero import Buzzer, Button, LED
import time
from signal import pause
bz = Buzzer(5)
bz.off()
led = LED(6)
led.off()
button = Button(21)

def buznlighton():
    led.on()
    bz.on()
    
def buznlightoff():
    led.off()
    bz.off()

button.when_pressed = buznlighton
button.when_released = buznlightoff


pause()




#Distance sensor
from gpiozero import DistanceSensor
import time

uds = DistanceSensor(trigger=21, echo=12)
while True:
    print(uds.distance)
    time.sleep(1)




#PIR sensor
from gpiozero import MotionSensor
import time

pir = MotionSensor(21)

while True:
    pir.wait_for_motion()
    print("Motion Detected!!")
    time.sleep(2)




#Light Detection Resistor
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
ldr = 16
GPIO.setup(ldr, GPIO.IN)
try:
    while True:
        if GPIO.input(ldr):
            print("Light detected")
        else:
            print("it is dark")
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopped")
finally:
    GPIO.cleanup()
Not working




#Make some noise
from gpiozero import Buzzer
import time
bz = Buzzer(26)
bz.on()
time.sleep(1)
bz.off()




#RFID sensor - requires additional file for import
from mfrc522 import WS1850S
import time
rfid = WS1850S()
print("WS1850S initialized, waiting for card...")
while True:
    if rfid.is_new_card_present():
        uid = rfid.read_card_uid()
        if uid:
            print(f"Card UID: {' '.join([f'{b:02X}' for b in uid])}")
        time.sleep(0.5)
    time.sleep(0.1)

#for installing and removing GPIO libraries
sudo apt remove python3-rpi-lgpio
sudo apt install python3-rpi.gpio

sudo apt remove python3-rpi.gpio
sudo apt install python3-rpi-lgpio




#night light
import RPi.GPIO as GPIO
from gpiozero import LED
import time

led = LED(26)
led.on()
GPIO.setmode(GPIO.BCM)

ldr = 5 
GPIO.setup(ldr, GPIO.IN)

try:
    while True:
        if GPIO.input(ldr):
            print("Light detected")
            led.off()
        else:
            print("it is dark")       
            led.on()
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopped")
finally:
    GPIO.cleanup()



#Take a picture using the camera
from picamera2 import Picamera2, Preview
import time

# Initialize the camera
picam2 = Picamera2()

# Create a configuration for the camera preview
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)

# Start the camera preview
picam2.start_preview(Preview.QTGL)
picam2.start()

# Allow time for the camera to adjust
time.sleep(5)

picam2.stop_preview()

# Capture an image and save it to a file
#picam2.capture_file("test_photo.jpg")
#picam2.stop()




#Button to capture photo
from picamera2 import Picamera2, Preview
import time
from datetime import datetime
from gpiozero import Button
from signal import pause
picam2 = Picamera2()
button = Button(17)
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
def capture():
    picam2.start_preview(Preview.QTGL)
    timestamp = datetime.now().isoformat()
    picam2.start()
    time.sleep(2)
    picam2.capture_file('/home/pi/%s.jpg' % timestamp)
    picam2.stop_preview()
    picam2.stop()
button.when_pressed = capture
pause()




#record a short video
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import time

picam2 = Picamera2()

video_config = picam2.create_video_configuration(
    main={"size": (1920, 1080)},
    lores={"size": (640, 480)},
    display="lores"
)
picam2.configure(video_config)

encoder = H264Encoder(bitrate=10_000_000)

# Use FfmpegOutput to wrap H.264 into MP4
output = FfmpegOutput("test.mp4")

picam2.start_preview(Preview.QTGL)
picam2.start_recording(encoder, output)

time.sleep(10)

picam2.stop_recording()
picam2.stop_preview()




#Control LCD1602 display requires additional file to import
import LCD1602v1
import time
import math

lcd=LCD1602v1.LCD1602(16,2)

try:
    while True:
        # set the cursor to column 0, line 1
        lcd.setCursor(0, 0)

        lcd.printout("Code Club")

        lcd.setCursor(0, 1)

        lcd.printout("Rocks!")
        time.sleep(0.1)
except(KeyboardInterrupt):
    lcd.clear()
    del lcd




#Potentiometer via MCP3008 chip

from gpiozero import MCP3008
from gpiozero import LED
import time

ledgrn = LED(26)
ledamb = LED(19)
ledred = LED(13)

pot = MCP3008(channel=0)
print(pot.value)

try:
    while True:
        percent = int(pot.value*100)
        print(f"%{percent}")
        if percent >3 and percent <50:
            ledgrn.on()
            ledamb.off()
            ledred.off()
        elif percent >50 and percent  <80:
            ledgrn.on()
            ledamb.on()
            ledred.off()
        elif percent >80:
            ledgrn.on()
            ledamb.on()
            ledred.on()
        else:
            ledgrn.off()
            ledamb.off()
            ledred.off()
        time.sleep(1)
except(KeyboardInterrupt):
    print("Stopped")
    ledgrn.off()
    ledamb.off()
    ledred.off()




#Alternative Potentiometer via MCP3008 using graph
from gpiozero import LEDBarGraph, MCP3008
from signal import pause

graph = LEDBarGraph(26, 19, 13, pwm=True)
pot = MCP3008(channel=0)
graph.source = pot
pause()
'''