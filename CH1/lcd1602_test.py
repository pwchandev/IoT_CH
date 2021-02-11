# import the necessary package
import RPi_I2C_driver as lcd1602
from time import *

mylcd = lcd1602.lcd()
mylcd.lcd_display_string("Hello World!",1)
mylcd.lcd_display_string("Test LCD1602",2,3)
sleep(10)
mylcd.lcd_clear()
