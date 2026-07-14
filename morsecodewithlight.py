from gpiozero import Buzzer, Button, LED, LEDBarGraph, MCP3008
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
#button.when_pressed = bz.on

button.when_released = buznlightoff
#button.when_released = bz.off

#Potentiometer display
graph = LEDBarGraph(12, pwm=True)
pot = MCP3008(channel=0)
graph.source = pot

#Control LCD1602 display requires additional file to import
import LCD1602
import time
import math

lcd=LCD1602.LCD1602(16,2)

try:
    while True:
        # set the cursor to column 0, line 1
        lcd.setCursor(0, 0)
        lcd.printout("Code Clubs at")
        lcd.setCursor(0, 1)
        lcd.printout("Morgan Stanley")
        time.sleep(5)
        lcd.clear()
        
        lcd.setCursor(0, 0)
        lcd.printout("St Mungo's")
        lcd.setCursor(0, 1)
        lcd.printout("Academy")
        time.sleep(5)
        lcd.clear()
        
        lcd.setCursor(0, 0)
        lcd.printout("Hillhead")
        lcd.setCursor(0, 1)
        lcd.printout("Primary School")
        time.sleep(5)
        lcd.clear()
        
        lcd.setCursor(0, 0)
        lcd.printout("Oakgrove")
        lcd.setCursor(0, 1)
        lcd.printout("Primary School")
        time.sleep(5)
        lcd.clear()
        
        lcd.setCursor(0, 0)
        lcd.printout("When's the time")
        lcd.setCursor(0, 1)
        lcd.printout("to join STEM?")
        time.sleep(5)
        lcd.clear()
        
        lcd.setCursor(0, 0)

        # Get the current local time as a list
        T = list(time.localtime())

        # Adjust the day of the week index (+1 to make it 1-indexed)
        T[6] += 1

        # Format each element in the time list as zero-padded 2-digit strings
        T = ["{:0>2}".format(str(i)) for i in T]

        # Display the date (year, month, day, day of the week) on the first row
        lcd.printout(T[0] + ' ' + T[1] + ' ' + T[2])

        # Set the cursor to column 0, row 1
        lcd.setCursor(0, 1)

        # Display the time (hours, minutes, seconds) on the second row
        lcd.printout(T[3] + ":" + T[4] + ":" + T[5])

        # Pause for 0.1 seconds before updating the display
        time.sleep(5)
        

        
except(KeyboardInterrupt):
    lcd.clear()
    del lcd
    
pause()