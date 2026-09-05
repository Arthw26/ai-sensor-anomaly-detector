import csv
import matplotlib.pyplot as plt

data = []

with open("python/data/sensor_data.csv", "r") as f:
    reader = csv.reader(f)

    for row in reader:
        if len(row) == 4 and row[0] == "DATA":
            data.append({
                "sample": int(row[1]),
                "temperature": float(row[2]),
                "current": float(row[3])
            })

samples = [d["sample"] for d in data]
temperatures = [d["temperature"] for d in data]
currents = [d["current"] for d in data]

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(samples, temperatures, marker="o", label="Temperature (C)")
ax1.set_xlabel("Sample")
ax1.set_ylabel("Temperature (C)")
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(samples, currents, marker="x", label="Current (A)")
ax2.set_ylabel("Current (A)")

plt.title("Virtual Embedded Device - Sensor Data")
fig.tight_layout()

plt.savefig("python/data/sensor_plot.png", dpi=150)
print(f"Saved {len(data)} samples to python/data/sensor_plot.png")
