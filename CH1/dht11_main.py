# import the necessary package
import dht11
import time
from math import trunc
import RPi_I2C_driver as lcd1602
import thingspeak

# DHT object setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
DHT_SENSOR = dht11.DHT11(pin=4)

# LCD1602 object setup
mylcd = lcd1602.lcd()

# ThingSpeak settings and setup
channel_id = 1213704  # PUT CHANNEL ID HERE
write_key  = 'DANCKY7NWP0IR2B9' # PUT YOUR WRITE KEY HERE
channel = thingspeak.Channel(id=channel_id, api_key=write_key)
wait_time = 15    # set wait time in seconds for update (min 15s-free account)

def wait(send_data, last_time, wait_time):
    if not send_data: 
        cur_time = trunc(time.time())
        # wait more than 15 seconds before sending data
        if cur_time > last_time + wait_time:
            send_data = True
            last_time = cur_time 
    return send_data, last_time 

def thing(temperature, humidity, send_data):
    if send_data:
        # write to thingspeak
        response = channel.update({'field1': temperature, 'field2': humidity})
        # read from thingspeak
        # read = channel.get({})
        read_t = eval(channel.get_field_last(1)) # convert string to dictionary
        read_temp = read_t['field1']
        read_h = eval(channel.get_field_last(2)) # convert string to dictionary
        read_humidity = read_h['field2']
        print(time.ctime())
        print(f'WRITE ThingSpeak temperature: {read_temp}C')
        print(f'WRITE ThingSpeak humidity: {read_humidity}%')
        send_data = False
    return send_data
       
if __name__ == '__main__':
    send_data = True
    last_time = trunc(time.time())
    try:
        while True:
            send_data, last_time = wait(send_data, last_time, wait_time)
            result = DHT_SENSOR.read()
            temperature = result.temperature
            humidity = result.humidity
            if result.is_valid():
                print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
                msg1 = 'Temp:     ' + str(round(temperature, 2)) + 'C'
                msg2 = 'Humidity: ' + str(round(humidity, 2)) + '%'
                mylcd.lcd_clear()
                mylcd.lcd_display_string(msg1, 1)
                mylcd.lcd_display_string(msg2, 2)
                send_data = thing(temperature, humidity, send_data)
            else:
                print("Sensor failure. Check wiring.");
            # DHT sensor need 2.5 seconds to settle down for new reading
            time.sleep(2.5)
            
    except KeyboardInterrupt:
        print('Press Ctrl-C to exit the program')
        mylcd.lcd_clear()
    
    
