import RPi.GPIO as GPIO
from time import sleep

LED1 = 17
LED2 = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)          # Number GPIOs by its logical location
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

def light_led(pin, status):
    if status:
        GPIO.output(pin, 1)         # Turn on LED
    else:
        GPIO.output(pin, 0)         # Turn off LED

def main():
    while True:
        print('Both LEDs - ON for 3 sec')
        light_led(LED1, True)
        light_led(LED2, True)
        sleep(3)
        print('LED1 - ON for 3 sec while LED 2 - OFF')
        light_led(LED1, True)
        light_led(LED2, False)
        sleep(3)
        print('LED2 - ON for 3 sec while LED 1 - OFF')
        light_led(LED1, False)
        light_led(LED2, True)
        sleep(3)
        print('Both LEDs - OFF for 3 sec')
        light_led(LED1, False)
        light_led(LED2, False)
        sleep(3)

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        pass

    finally:
        print('Program end ...')
        GPIO.cleanup()