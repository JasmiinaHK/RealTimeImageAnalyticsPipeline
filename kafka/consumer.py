import cv2
import numpy as np
import os
import json
from kafka import KafkaConsumer
from sklearn.cluster import KMeans
import urllib.request

# YOLOv4-tiny model URLs and file paths
CFG_URL = "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg"
WEIGHTS_URL = "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights"
CFG_PATH = "yolov4-tiny.cfg"
WEIGHTS_PATH = "yolov4-tiny.weights"

# Download model files if missing
def download_file(url, destination):
    if not os.path.exists(destination):
        print(f"📥 Downloading {destination}...")
        urllib.request.urlretrieve(url, destination)
        print("✅ Download complete.")

download_file(CFG_URL, CFG_PATH)
download_file(WEIGHTS_URL, WEIGHTS_PATH)

# Load model
net = cv2.dnn.readNetFromDarknet(CFG_PATH, WEIGHTS_PATH)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# COCO class labels
COCO_NAMES = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus",
    "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon",
    "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
    "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard",
    "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

# Kafka consumer setup
consumer = KafkaConsumer(
    'image_paths',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

results = []

print("🚀 YOLOv4-tiny Consumer ready and listening to Kafka topic...")

def detect_objects(image, conf_threshold=0.3, nms_threshold=0.4):
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    ln = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(ln)

    boxes = []
    confidences = []
    class_ids = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                box = detection[0:4] * np.array([w, h, w, h])
                (centerX, centerY, bw, bh) = box.astype("int")
                x = int(centerX - (bw / 2))
                y = int(centerY - (bh / 2))
                boxes.append([x, y, int(bw), int(bh)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    objects = []
    if len(idxs) > 0:
        for i in idxs.flatten():
            label = COCO_NAMES[class_ids[i]]
            confidence = confidences[i]
            box = boxes[i]
            objects.append({
                "label": label,
                "confidence": confidence,
                "box": box
            })
    return objects

def get_dominant_colors(image, k=3):
    # Resize image to reduce memory usage before KMeans
    resized = cv2.resize(image, (100, 100))  # 100x100 is usually enough
    pixels = resized.reshape((-1, 3)).astype(np.float32)

    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int).tolist()
    return colors

# Start consuming images
for msg in consumer:
    image_path = msg.value['image_path']
    print(f"\n📥 Received: {image_path}")
    full_path = os.path.abspath(image_path)

    if not os.path.exists(full_path):
        print(f"❌ Image not found: {full_path}")
        continue

    image = cv2.imread(full_path)
    if image is None:
        print(f"❌ Failed to load image: {full_path}")
        continue

    print("🔍 Running YOLOv4-tiny object detection...")
    detected_objects = detect_objects(image)

    print("🎨 Extracting dominant colors...")
    dominant_colors = get_dominant_colors(image, k=3)

    metadata = {
        "image_path": full_path,
        "recognized_objects": detected_objects,
        "dominant_colors": dominant_colors
    }

    results.append(metadata)

    with open("metadata_output.json", "w") as f:
        json.dump(results, f, indent=4)

    print(f"✅ Processed and saved: {image_path}")
