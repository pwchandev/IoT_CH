import RPi.GPIO as GPIO
import dht11
import RPi_I2C_driver as lcd1602
import time
 
# initial setup of LCD1602 and DHT11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
DHT_SENSOR = dht11.DHT11(pin=4)
mylcd = lcd1602.lcd()

def main():
    while True:
        result = DHT_SENSOR.read()
        temperature = result.temperature
        humidity = result.humidity
        if result.is_valid():
            print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
            mylcd.lcd_clear()
            msg1 = 'Temp: ' + str(round(temperature, 2)) + 'C'
            msg2 = 'Humidity: ' + str(round(humidity, 2)) + '%'
            mylcd.lcd_display_string(msg1,1)
            mylcd.lcd_display_string(msg2,2)
        else:
            print("Sensor failure. Check wiring.");
        time.sleep(3)

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt: 
        pass

    finally:
	    GPIO.cleanup()
	    print('The end !')
