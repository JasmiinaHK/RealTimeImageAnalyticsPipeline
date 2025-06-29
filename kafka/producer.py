from kafka import KafkaProducer
import os
import json
import time

# Kafka producer initialization
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Folder with images
image_folder = "images_subset"

# Kafka topic
topic_name = "image_paths"

# Sending images one by one
for filename in os.listdir(image_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(image_folder, filename)
        message = {
            "image_path": image_path,
            "timestamp": time.time()
        }
        producer.send(topic_name, message)
        print(f"Sent: {message}")

producer.flush()
