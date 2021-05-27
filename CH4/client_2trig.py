
import RPi.GPIO as GPIO
from datetime import datetime
import asyncio
import os
from dotenv import load_dotenv
from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodResponse

# The connection details from IoT Central for the device
load_dotenv()
id_scope = os.getenv("ID_SCOPE")
primary_key = os.getenv("PRIMARY_KEY")
device_id = "pi-environment-client"

# initial setup 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
LED1 = 17
LED2 = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)          # Number GPIOs by its logical location
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

async def light_led(pin, time):
    GPIO.output(pin, 1)         # Turn on LED
    await asyncio.sleep(time)
    GPIO.output(pin, 0)         # Turn off LED

# Asynchronously wait for commands from IoT Central
# If the TooBright command is called, handle it
async def light_listener(device_client):
    # Wait for commands from IoT Central
    method_request = await device_client.receive_method_request("TooBright")
    # Log that the command was received
    timestamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M %S'), '%Y-%m-%d %H:%M %S')
    print(timestamp, end='')
    print(" Too Bright Command handled")
    # Asynchronously light the LED
    # This will be run in the background, so the result can
    # be returned to IoT Central straight away, not 10 seconds later
    asyncio.gather(light_led(LED1, 10))
    # IoT Central expects a response from a command, saying if the call
    # was successful or not, so send a success response
    payload = {"result": True}
    # Build the response
    method_response = MethodResponse.create_from_method_request(
        method_request, 200, payload
    )
    # Send the response to IoT Central
    await device_client.send_method_response(method_response)

# Asynchronously wait for commands from IoT Central
# If the TooHot command is called, handle it
async def temp_listener(device_client):
    # Wait for commands from IoT Central
    method_request = await device_client.receive_method_request("TooHot")
    # Log that the command was received
    timestamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M %S'), '%Y-%m-%d %H:%M %S')
    print(timestamp, end='')
    print(" Too Hot Command handled")
    # Asynchronously light the LED
    # This will be run in the background, so the result can
    # be returned to IoT Central straight away, not 10 seconds later
    asyncio.gather(light_led(LED2, 10))
    # IoT Central expects a response from a command, saying if the call
    # was successful or not, so send a success response
    payload = {"result": True}
    # Build the response
    method_response = MethodResponse.create_from_method_request(
        method_request, 200, payload
    )
    # Send the response to IoT Central
    await device_client.send_method_response(method_response)

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
    timestamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M %S'), '%Y-%m-%d %H:%M %S')
    print(timestamp, end='')
    print(" Connecting ...")
    await device_client.connect()
    timestamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M %S'), '%Y-%m-%d %H:%M %S')
    print(timestamp, end='')
    print(" Connected!")

    # Start the command listener
    timestamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M %S'), '%Y-%m-%d %H:%M %S')
    print(timestamp, end='')
    print(" Start Listening ...")
    listener1 = asyncio.gather(light_listener(device_client))
    listener2 = asyncio.gather(temp_listener(device_client))
    # async loop
    async def main_loop():
        while True:
            await asyncio.sleep(60)
            listener1 = asyncio.gather(light_listener(device_client))
            listener2 = asyncio.gather(temp_listener(device_client))

    # Run the async main loop forever
    try:
        await main_loop()

    except KeyboardInterrupt:
        # Cancel listening
        listener1.cancel()
        listener2.cancel()

    finally:
        # Finally, disconnect
        await device_client.disconnect()
        timestamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M %S'), '%Y-%m-%d %H:%M %S')
        print(timestamp, end='')
        print(" Disconnected!")
        GPIO.cleanup()

# Start the program running
asyncio.run(main())