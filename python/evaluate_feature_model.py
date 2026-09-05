import csv
from pathlib import Path

import joblib
from sklearn.metrics import confusion_matrix

from feature_extraction import extract_features


DATASET = Path("python/data/synthetic_sensor_data.csv")
MODEL = Path("python/models/anomaly_detector_feature_based.joblib")
WINDOW_SIZE = 10


def load_runs():
    runs = {}

    with DATASET.open(newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            run = int(row["run"])

            runs.setdefault(run, []).append({
                "sample": int(row["sample"]),
                "temperature": float(row["temperature"]),
                "current": float(row["current"]),
                "vibration": float(row["vibration"]),
                "label": int(row["label"]),
            })

    return runs


model = joblib.load(MODEL)
runs = load_runs()

errors = []

for run in [9, 10]:
    samples = runs[run]

    for start in range(len(samples) - WINDOW_SIZE + 1):
        window = samples[start:start + WINDOW_SIZE]

        temperature = [x["temperature"] for x in window]
        current = [x["current"] for x in window]
        vibration = [x["vibration"] for x in window]

        features = extract_features(
            temperature,
            current,
            vibration,
        )

        expected = int(any(x["label"] for x in window))
        predicted = int(model.predict([features])[0])

        if expected != predicted:
            errors.append({
                "run": run,
                "start_sample": window[0]["sample"],
                "end_sample": window[-1]["sample"],
                "expected": expected,
                "predicted": predicted,
            })

y_true = []
y_pred = []

for run in [9, 10]:
    samples = runs[run]

    for start in range(len(samples) - WINDOW_SIZE + 1):
        window = samples[start:start + WINDOW_SIZE]

        features = extract_features(
            [x["temperature"] for x in window],
            [x["current"] for x in window],
            [x["vibration"] for x in window],
        )

        y_true.append(int(any(x["label"] for x in window)))
        y_pred.append(int(model.predict([features])[0]))

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

print("Feature-Based Error Analysis")
print("----------------------------")
print(f"True positives : {tp}")
print(f"True negatives : {tn}")
print(f"False positives: {fp}")
print(f"False negatives: {fn}")
print(f"Total errors   : {len(errors)}")
print()

for error in errors:
    print(
        f"run={error['run']} "
        f"window={error['start_sample']}-{error['end_sample']} "
        f"expected={error['expected']} "
        f"predicted={error['predicted']}"
    )
