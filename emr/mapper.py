#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    try:
        data = json.loads(line)
        for obj in data.get("recognized_objects", []):
            label = obj.get("label", "unknown")
            print(f"{label}\t1")
    except Exception as e:
        continue
