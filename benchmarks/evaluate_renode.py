import re
import subprocess

COMMAND = [
    "renode",
    "--plain",
    "--disable-xwt",
    "-e",
    '$elf="/home/embedded/ai_sensor_anomaly_detector/build_riscv/zephyr/zephyr.elf"; '
    'include @/home/embedded/ai_sensor_anomaly_detector/renode/anomaly_detector.resc; '
    "sleep 3; quit",
]

result = subprocess.run(
    COMMAND,
    capture_output=True,
    text=True,
    timeout=10,
)

output = result.stdout + result.stderr

fault_match = re.search(
    r"FAULT_WINDOWS,temp=(\d+),current=(\d+),vibration=(\d+)",
    output,
)

if not fault_match:
    raise RuntimeError("FAULT_WINDOWS line not found")

temp_start = int(fault_match.group(1))
current_start = int(fault_match.group(2))
vibration_start = int(fault_match.group(3))

rows = []

for line in output.splitlines():
    match = re.search(
        r"DATA,(\d+),[^,]+,[^,]+,[^,]+,(\d+)",
        line,
    )

    if match:
        rows.append({
            "sample": int(match.group(1)),
            "prediction": int(match.group(2)),
        })


def expected_label(sample):
    if temp_start <= sample < temp_start + 20:
        return 1
    if current_start <= sample < current_start + 10:
        return 1
    if vibration_start <= sample < vibration_start + 5:
        return 1
    return 0


y_true = [expected_label(row["sample"]) for row in rows]
y_pred = [row["prediction"] for row in rows]

tp = sum(a == 1 and b == 1 for a, b in zip(y_true, y_pred))
tn = sum(a == 0 and b == 0 for a, b in zip(y_true, y_pred))
fp = sum(a == 0 and b == 1 for a, b in zip(y_true, y_pred))
fn = sum(a == 1 and b == 0 for a, b in zip(y_true, y_pred))

accuracy = (tp + tn) / len(y_true)
precision = tp / (tp + fp) if tp + fp else 0.0
recall = tp / (tp + fn) if tp + fn else 0.0
f1 = (
    2 * precision * recall / (precision + recall)
    if precision + recall
    else 0.0
)

print("Renode Embedded Inference Evaluation")
print("------------------------------------")
print(f"Samples evaluated: {len(y_true)}")
print(f"Temperature fault: {temp_start}-{temp_start + 19}")
print(f"Current fault    : {current_start}-{current_start + 9}")
print(f"Vibration fault  : {vibration_start}-{vibration_start + 4}")
print()
print(f"Accuracy : {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall   : {recall:.3f}")
print(f"F1 Score : {f1:.3f}")
print(f"False positives: {fp}")
print(f"False negatives: {fn}")
print()
print(f"True positives : {tp}")
print(f"True negatives : {tn}")
