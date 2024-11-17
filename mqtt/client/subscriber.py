import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from confluent_kafka import Producer
import json

# Load environment variables from the .env file
load_dotenv()

# Read configurations strictly from the .env file
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# Ensure all required environment variables are provided
if not all([MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, KAFKA_BROKER, KAFKA_TOPIC]):
    raise EnvironmentError("Required environment variables are missing in the .env file.")

# Kafka Producer
def delivery_report(err, msg):
    """
    Callback function for Kafka delivery reports.

    Args:
        err (KafkaError): Error object if the message delivery fails.
        msg (Message): Kafka message object for successfully delivered messages.
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [Partition: {msg.partition()}]")

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    """
    Callback function triggered when the MQTT client connects to the broker.

    Args:
        client (mqtt.Client): MQTT client instance.
        userdata: User-defined data of any type.
        flags: Response flags sent by the broker.
        rc (int): Connection result (0 indicates success).
    """
    print("Connected to the MQTT Broker!")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    """
    Callback function triggered when a message is received from MQTT.

    Args:
        client (mqtt.Client): MQTT client instance.
        userdata: User-defined data of any type.
        msg (mqtt.MQTTMessage): Received MQTT message.
    """
    try:
        # Parse the MQTT message and send it to Kafka
        message = json.loads(msg.payload.decode())
        print(f"Received from MQTT: {message}")

        # Send the message to Kafka
        producer.produce(KAFKA_TOPIC, value=json.dumps(message), callback=delivery_report)
        producer.flush()  # Ensure all messages are sent
        print(f"Sent to Kafka: {message}")
    except Exception as e:
        print(f"Error processing the message: {e}")

def start_subscriber():
    """
    Starts the MQTT subscriber to receive messages and forward them to Kafka.
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT Broker
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()

if __name__ == "__main__":
    """
    Entry point of the program. Starts the MQTT subscriber.
    """
    start_subscriber()
