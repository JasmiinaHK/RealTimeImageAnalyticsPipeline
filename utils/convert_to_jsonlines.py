import json

with open("metadata_output.json", "r") as f:
    data = json.load(f)

with open("metadata_lines.json", "w") as f:
    for entry in data:
        f.write(json.dumps(entry) + "\n")
