from collections import Counter

with open("final_output.txt", "r") as f:
    lines = f.readlines()

counter = Counter()

for line in lines:
    try:
        label, count = line.strip().split()
        counter[label] += int(count)
    except:
        continue

top10 = counter.most_common(10)

print("🔝 Top 10 najčešće detektovanih objekata:")
for label, total in top10:
    print(f"{label}: {total}")
