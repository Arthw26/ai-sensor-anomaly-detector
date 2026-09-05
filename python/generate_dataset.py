import csv
import random

OUTPUT_FILE = "python/data/synthetic_sensor_data.csv"

random.seed(42)

SAMPLES_PER_RUN = 300
RUNS = 10

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "run",
        "sample",
        "temperature",
        "current",
        "vibration",
        "label",
    ])

    for run in range(1, RUNS + 1):
        temp_start = random.randint(20, 80)
        current_start = random.randint(100, 180)
        vibration_start = random.randint(200, 260)

        for sample in range(1, SAMPLES_PER_RUN + 1):

            # Normal operating ranges
            temperature = 25.0 + random.uniform(-1.5, 1.5)
            current = 5.0 + random.uniform(-0.40, 0.40)
            vibration = 1.0 + random.uniform(-0.25, 0.25)

            anomaly = False

            # Temperature fault
            if temp_start <= sample < temp_start + 20:
                temperature = 28.0 + random.uniform(-1.5, 1.5)
                anomaly = True

            # Current fault
            if current_start <= sample < current_start + 10:
                current = 5.8 + random.uniform(-0.40, 0.40)
                anomaly = True

            # Vibration fault
            if vibration_start <= sample < vibration_start + 5:
                vibration = 1.4 + random.uniform(-0.25, 0.25)
                anomaly = True

            writer.writerow([
                run,
                sample,
                round(temperature, 2),
                round(current, 2),
                round(vibration, 2),
                int(anomaly),
            ])

print(f"Generated {RUNS} runs with {SAMPLES_PER_RUN} samples each.")
print(f"Saved to {OUTPUT_FILE}")
