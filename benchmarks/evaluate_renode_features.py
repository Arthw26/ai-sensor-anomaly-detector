import re
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ELF = PROJECT_ROOT / "build_riscv" / "zephyr" / "zephyr.elf"
RESC = PROJECT_ROOT / "renode" / "anomaly_detector.resc"

if not ELF.exists():
    raise FileNotFoundError(f"Renode ELF not found: {ELF}")

if not RESC.exists():
    raise FileNotFoundError(f"Renode script not found: {RESC}")

command = [
    "renode",
    "--plain",
    "--disable-xwt",
    "-e",
    f'$elf="{ELF}"; include @{RESC}; sleep 3; quit',
]

result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    timeout=30,
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

predictions = []

feature_window = 0

for line in output.splitlines():
    match = re.search(r"FEATURE_ANOMALY,(\d+)", line)

    if match:
        feature_window += 1
        window_start = (feature_window - 1) * 10 + 1
        window_end = window_start + 9

        predictions.append({
            "start": window_start,
            "end": window_end,
            "prediction": int(match.group(1)),
        })


def expected_label(start, end):
    fault_ranges = [
        (temp_start, temp_start + 19),
        (current_start, current_start + 9),
        (vibration_start, vibration_start + 4),
    ]

    for fault_start, fault_end in fault_ranges:
        if start <= fault_end and end >= fault_start:
            return 1

    return 0


if not predictions:
    raise RuntimeError("No FEATURE_ANOMALY samples found")

y_true = [
    expected_label(row["start"], row["end"])
    for row in predictions
]

y_pred = [
    row["prediction"]
    for row in predictions
]

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

print("Renode Feature-Based Evaluation")
print("--------------------------------")
print(f"Windows evaluated: {len(y_true)}")
print(f"Window size: 10 samples")
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
