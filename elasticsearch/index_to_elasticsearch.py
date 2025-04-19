from elasticsearch import Elasticsearch
import json
from datetime import datetime

es = Elasticsearch("http://localhost:9200")
index_name = "image_metadata"

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

with open("metadata_lines.json", "r") as f:
    for line in f:
        doc = json.loads(line)
        doc["timestamp"] = datetime.now().isoformat()  # ➕ dodaj timestamp
        es.index(index=index_name, document=doc)

print("✅ Successfully indexed metadata into Elasticsearch!")
