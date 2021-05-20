
import RPi.GPIO as GPIO
import ADC0832
import dht11
import RPi_I2C_driver as lcd1602
from datetime import datetime
import asyncio
import json
import os
from dotenv import load_dotenv
from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient

# The connection details from IoT Central for the device
load_dotenv()
id_scope = os.getenv("ID_SCOPE")
primary_key = os.getenv("PRIMARY_KEY")
device_id = "pi-environment-monitor"

# initial setup of DHT11, LCD1602 and ADC0832 for photoresistor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
DHT_SENSOR = dht11.DHT11(pin=4)
mylcd = lcd1602.lcd()
ADC0832.setup()         

# Gets telemetry from the Grove sensors
# Telemetry needs to be sent as JSON data
async def get_telemetry() -> str:
    # The dht call returns the temperature and the humidity,
    result = DHT_SENSOR.read()
    temperature = result.temperature
    # The temperature can come as 0, meaning you are reading
    # too fast, if so sleep for a second to ensure the next reading
    # is ready
    while True:
        if result.is_valid():
            timestamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M %S'), '%Y-%m-%d %H:%M %S')
            print(timestamp, end='')
            print(" Temp={0:0.1f}C ".format(temperature))
            mylcd.lcd_clear()
            msg1 = 'Temp: ' + str(round(temperature, 2)) + 'C'
            mylcd.lcd_display_string(msg1,1)
            break
        else:
            result = DHT_SENSOR.read()
            temperature = result.temperature   
            await asyncio.sleep(1)

    # Build a dictionary of data
    # The items in the dictionary need names that match the
    # telemetry values expected by IoT Central
    dict = {
        "Temperature" : temperature,  # The temperature value
    }

    # Convert the dictionary to JSON
    return json.dumps(dict)

# The main function that runs the program in an async loop
async def main():
    # Connect to IoT Central and request the connection details for the device
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host="global.azure-devices-provisioning.net",
        registration_id=device_id,
        id_scope=id_scope,
        symmetric_key=primary_key)
    registration_result = await provisioning_device_client.register()

    # Build the connection string - this is used to connect to IoT Central
    conn_str="HostName=" + registration_result.registration_state.assigned_hub + \
                ";DeviceId=" + device_id + \
                ";SharedAccessKey=" + primary_key

    # The client object is used to interact with Azure IoT Central.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    print("Connecting")
    await device_client.connect()
    print("Connected")

    # async loop that sends the telemetry
    async def main_loop():
        while True:
            # Get the telemetry to send
            telemetry = await get_telemetry()
            print("Telemetry:", telemetry)

            # Send the telemetry to IoT Central
            await device_client.send_message(telemetry)

            # Wait for a minute so telemetry is not sent to often
            await asyncio.sleep(60)

    # Run the async main loop forever
    await main_loop()

    # Finally, disconnect
    await device_client.disconnect()

# Start the program running
asyncio.run(main())