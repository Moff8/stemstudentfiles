from mfrc522 import WS1850S
from gpiozero import Buzzer, LED
import time
import os
led = LED(16)
rfid = WS1850S()
bz = Buzzer(20)

print("WS1850S initialized, waiting for card...")
try:
    while True:
        if rfid.is_new_card_present():
            uid = rfid.read_card_uid()
            if uid:
                print(f"Card UID: {' '.join([f'{b:02X}' for b in uid])}")
                print("Card recognised - Welcome to work ;)")
                bz.on()
                time.sleep(0.1)
                bz.off()
                led.on()
                time.sleep(1)
                led.off()
                time.sleep(2)
                os.system("clear")
                print("WS1850S initialized, waiting for card...")
            time.sleep(0.5)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped")