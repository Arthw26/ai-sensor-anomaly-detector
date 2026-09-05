import csv
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier, export_text

from feature_extraction import extract_features


DATASET = Path("python/data/synthetic_sensor_data.csv")
MODEL_DIR = Path("python/models")
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


def build_windows(samples):
    features = []
    labels = []

    for start in range(0, len(samples) - WINDOW_SIZE + 1):
        window = samples[start:start + WINDOW_SIZE]

        temperature = [row["temperature"] for row in window]
        current = [row["current"] for row in window]
        vibration = [row["vibration"] for row in window]

        features.append(
            extract_features(temperature, current, vibration)
        )

        labels.append(
            int(any(row["label"] for row in window))
        )

    return features, labels


runs = load_runs()

train_features = []
train_labels = []
test_features = []
test_labels = []

for run, samples in runs.items():
    features, labels = build_windows(samples)

    if run <= 8:
        train_features.extend(features)
        train_labels.extend(labels)
    else:
        test_features.extend(features)
        test_labels.extend(labels)


model = RandomForestClassifier(
    n_estimators=50,
    max_depth=5,
    random_state=42,
)

model.fit(train_features, train_labels)

predictions = model.predict(test_features)

print("Feature-Based Anomaly Detector")
print("--------------------------------")
print(f"Window size: {WINDOW_SIZE}")
print(f"Training windows: {len(train_features)}")
print(f"Test windows: {len(test_features)}")
print()
print(f"Accuracy : {accuracy_score(test_labels, predictions):.3f}")
print(f"Precision: {precision_score(test_labels, predictions, zero_division=0):.3f}")
print(f"Recall   : {recall_score(test_labels, predictions, zero_division=0):.3f}")
print(f"F1 Score : {f1_score(test_labels, predictions, zero_division=0):.3f}")
print()
print("Feature importances:")
names = [
    "temp_mean",
    "temp_variance",
    "temp_peak_to_peak",
    "temp_max",
    "current_mean",
    "current_variance",
    "current_peak_to_peak",
    "current_max",
    "vibration_mean",
    "vibration_variance",
    "vibration_peak_to_peak",
    "vibration_max",
    "vibration_rms",
]

for name, importance in zip(names, model.feature_importances_):
    print(f"  {name:25s}: {importance:.3f}")

MODEL_DIR.mkdir(parents=True, exist_ok=True)

import joblib

output = MODEL_DIR / "anomaly_detector_feature_based.joblib"
joblib.dump(model, output)

print()
print(f"Saved model: {output}")
