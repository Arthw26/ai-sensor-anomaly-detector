import csv

input_file = "python/data/sensor_data.csv"
output_file = "python/data/training_data.csv"

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    writer.writerow(["sample", "temperature", "current", "label"])

    for row in reader:
        if len(row) != 4 or row[0] != "DATA":
            continue

        sample = int(row[1])
        temperature = float(row[2])
        current = float(row[3])

        label = 1 if (8 <= sample <= 12) or (20 <= sample <= 24) else 0

        writer.writerow([sample, temperature, current, label])

print(f"Created {output_file}")
