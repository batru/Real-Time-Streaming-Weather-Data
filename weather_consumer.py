from confluent_kafka import Consumer, KafkaError,KafkaException
from app import load_data
from dotenv import load_dotenv
import os
import json
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv() # Load env 
uri = os.getenv('DB_STRING')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


# Kafka Consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker(s)
    'group.id': 'weather-consumer-group',  # Consumer group ID
    'auto.offset.reset': 'earliest'  # Start consuming from the earliest message
}

# Create Consumer instance
consumer = Consumer(conf)

# Kafka topic to consume messages from
topic = 'weather_topic'

# Subscribe to the topic
consumer.subscribe([topic])

# Delivery callback to handle message processing
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


# Main consumer loop
while True:
    try:
        # Poll for a message (timeout )
        msg = consumer.poll(180.0)  # 3 minutes timeout

        if msg is None:
            print("No message received within the timeout period.")
        elif msg.error():
            # Handle errors from the consumer
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"End of partition reached: {msg.partition()} at offset {msg.offset()}")
            else:
                raise KafkaException(msg.error())
        else:
            # Successfully received a message
            print(f"Received message: {msg.value().decode('utf-8')}")

            # Deserialize the message (assuming the message is in JSON format)
            message_data = json.loads(msg.value().decode('utf-8'))

            # Load data in db
            load_data([message_data]) #list message data

            # Optional: You can print or handle the processed data here
            print(f"Processed data: {message_data}")

            time.sleep(180) 

    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        break
   