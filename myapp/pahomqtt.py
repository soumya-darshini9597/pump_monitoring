import time
import paho.mqtt.client as mqtt
from .models import Quantity 
import re
from myapp.models import Quantity 

# MQTT Configuration
MQTT_BROKER = 'mqttbroker.bc-pl.com'
MQTT_PORT = 1883  
MQTT_TOPIC = '123/pump'
MQTT_USER = 'mqttuser'
MQTT_PASSWORD = 'Bfl@2025'

# Callback when connected to broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker.")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect. Code: {rc}")



# Callback when message is received
# def on_message(client, userdata, msg):
#     try:
#         payload = msg.payload.decode('utf-8')  
#         print(payload)
#         Quantity.objects.create(quantity=payload) 

#     except Exception as e:
#         print(f"Error handling message: {e}")



def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8').strip()
        print(f"Received: {payload}")

        match = re.search(r'=\s*(\d+)', payload)
        if match:
            value = int(match.group(1))
            Quantity.objects.create(quantity=value)
            print(f"Saved value: {value}")
        else:
            print("No numeric value found in message.")

    except Exception as e:
        print(f"Error handling message: {e}")

        print(f"Error handling message: {e}")


# MQTT connection starter
def mqtt_connect():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"Failed to connect to broker: {e}")
        return
    client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")
        client.loop_stop()
        client.disconnect()
