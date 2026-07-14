from gpiozero import LED
from time import sleep
red = LED(13)
amber = LED(19)
green = LED(26)

while True:
    red.on()
    amber.on()
    green.on()
    sleep(1)
    
    red.off()
    amber.on()
    green.on()
    sleep(1)
    
    red.off()
    amber.off()
    green.off()
    sleep(1)
    
        
    
    
    


    