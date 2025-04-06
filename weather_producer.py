from confluent_kafka import Producer
from app import extract_data, transform_data
import json
import time

conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}

producer = Producer(conf)
topic = 'weather_topic'



# Delivery callback
def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")



while True:
    #call functions
    extracted_data = extract_data()
    data = transform_data(extracted_data)

    for record in data:
        producer.produce(topic,  value=json.dumps(record), callback=delivery_report)
        producer.poll(0) # Trigger delivery callback

        

    time.sleep(600) #after 10 minutes
