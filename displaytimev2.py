#Control LCD1602 display requires additional file to import
import LCD1602
import time
import math
from datetime import datetime
from zoneinfo import ZoneInfo

lcd=LCD1602.LCD1602(16,2)

try:
    while True:
        utc_time = datetime.now(ZoneInfo("Europe/London"))
        ny_time = datetime.now(ZoneInfo("America/New_York"))
        hongkong_time = datetime.now(ZoneInfo("Asia/Hong_Kong"))
        kolkata_time = datetime.now(ZoneInfo("Asia/Kolkata"))

        ln = (f"Lon: {utc_time.strftime('%a %H:%M')}")
        ny = (f"NY : {ny_time.strftime('%a %H:%M')}")
        hk = (f"HK : {hongkong_time.strftime('%a %H:%M')}")
        ist = (f"IST: {kolkata_time.strftime('%a %H:%M')}")
        # set the cursor to column 0, line 1
        lcd.setCursor(0, 0)

        lcd.printout(hk)

        lcd.setCursor(0, 1)

        lcd.printout(ist)
        time.sleep(12)
        lcd.clear()
        
        lcd.setCursor(0, 0)

        lcd.printout(ln)

        lcd.setCursor(0, 1)

        lcd.printout(ny)
        time.sleep(12)
        lcd.clear()
        
        
        
except(KeyboardInterrupt):
    lcd.clear()
    del lcd



