import re
import subprocess

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

EXECUTABLE = "./build/zephyr/zephyr.exe"

result = subprocess.run(
    ["timeout", "--signal=KILL", "3", EXECUTABLE],
    capture_output=True,
    text=True,
)

output = result.stdout

match = re.search(
    r"FAULT_WINDOWS,temp=(\d+),current=(\d+),vibration=(\d+)",
    output,
)

if not match:
    raise RuntimeError("FAULT_WINDOWS line not found")

temp_start = int(match.group(1))
current_start = int(match.group(2))
vibration_start = int(match.group(3))

embedded_rows = []

for line in output.splitlines():
    if not line.startswith("DATA,"):
        continue

    parts = line.split(",")

    if len(parts) != 6:
        continue

    embedded_rows.append({
        "sample": int(parts[1]),
        "prediction": int(parts[5]),
    })


def expected_label(sample):
    if temp_start <= sample < temp_start + 20:
        return 1
    if current_start <= sample < current_start + 10:
        return 1
    if vibration_start <= sample < vibration_start + 5:
        return 1
    return 0


y_true = [expected_label(row["sample"]) for row in embedded_rows]
y_pred = [row["prediction"] for row in embedded_rows]

print("Embedded C inference evaluation")
print("--------------------------------")
print(f"Samples evaluated: {len(y_true)}")
print(f"Temperature fault: {temp_start}-{temp_start + 19}")
print(f"Current fault    : {current_start}-{current_start + 9}")
print(f"Vibration fault  : {vibration_start}-{vibration_start + 4}")
print()
print(f"Accuracy : {accuracy_score(y_true, y_pred):.3f}")
print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.3f}")
print(f"Recall   : {recall_score(y_true, y_pred, zero_division=0):.3f}")
print(f"F1 Score : {f1_score(y_true, y_pred, zero_division=0):.3f}")
print(f"False positives: {sum(a == 0 and b == 1 for a, b in zip(y_true, y_pred))}")
print(f"False negatives: {sum(a == 1 and b == 0 for a, b in zip(y_true, y_pred))}")
