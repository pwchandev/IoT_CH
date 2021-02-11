import RPi.GPIO as GPIO
import dht11
import time
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
DHT_SENSOR = dht11.DHT11(pin=4)
 
while True:
    result = DHT_SENSOR.read()
    temperature = result.temperature
    humidity = result.humidity
    if result.is_valid():
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor failure. Check wiring.");
    time.sleep(3);

GPIO.cleanup()