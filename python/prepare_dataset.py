import csv

input_file = "python/data/sensor_data.csv"
output_file = "python/data/training_data.csv"

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    writer.writerow(["sample", "temperature", "current", "vibration", "label"])

    for row in reader:
        if len(row) != 5 or row[0] != "DATA":
            continue

        sample = int(row[1])
        temperature = float(row[2])
        current = float(row[3])
        vibration = float(row[4])

        label = 1 if (14 <= sample <= 33) or (40 <= sample <= 49) or (30 <= sample <= 34) else 0

        writer.writerow([
            sample,
            temperature,
            current,
            vibration,
            label
        ])

print(f"Created {output_file}")
