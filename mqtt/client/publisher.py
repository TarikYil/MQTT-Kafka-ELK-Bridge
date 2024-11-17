import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import pandas as pd
import seaborn as sns
import json
import time

# Load environment variables from the .env file
load_dotenv()

# Read configurations strictly from the .env file
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# Ensure all required environment variables are provided
if not all([MQTT_BROKER, MQTT_PORT, MQTT_TOPIC]):
    raise EnvironmentError("Required environment variables are missing in the .env file.")

# Load example dataset
data = sns.load_dataset("tips")

def publish_data():
    """
    Publishes data from the `tips` dataset to an MQTT broker cyclically.

    The function sends one row of data at a time, appends a timestamp to it, 
    and publishes the message to the specified MQTT topic.

    Raises:
        Exception: If there is an issue with publishing the data.
    """
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT)
    
    index = 0
    while True:
        try:
            # Prepare data for publishing
            record = data.iloc[index % len(data)].to_dict()  # Cyclic data sending
            record["timestamp"] = time.time()
            message = json.dumps(record)
            
            # Publish the message to the MQTT topic
            client.publish(MQTT_TOPIC, message)
            print(f"Published: {message}")
            index += 1
            
            time.sleep(1)  # Delay between messages
        except Exception as e:
            print(f"Error publishing data: {e}")
            break

if __name__ == "__main__":
    """
    Entry point of the program. Starts the MQTT publisher.
    """
    publish_data()
