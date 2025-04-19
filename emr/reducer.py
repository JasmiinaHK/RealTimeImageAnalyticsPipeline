#!/usr/bin/env python3
import sys

current_label = None
current_count = 0

for line in sys.stdin:
    label, count = line.strip().split('\t')
    count = int(count)

    if label == current_label:
        current_count += count
    else:
        if current_label:
            print(f"{current_label}\t{current_count}")
        current_label = label
        current_count = count

if current_label:
    print(f"{current_label}\t{current_count}")
