import csv
import joblib

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

DATA_FILE = "python/data/synthetic_sensor_data.csv"
MODEL_FILE = "python/models/anomaly_detector_synthetic.joblib"

data = []

with open(DATA_FILE, "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        data.append({
            "run": int(row["run"]),
            "temperature": float(row["temperature"]),
            "current": float(row["current"]),
            "vibration": float(row["vibration"]),
            "label": int(row["label"]),
        })

train_runs = set(range(1, 9))
test_runs = set(range(9, 11))

train_data = [d for d in data if d["run"] in train_runs]
test_data = [d for d in data if d["run"] in test_runs]

X_train = [
    [d["temperature"], d["current"], d["vibration"]]
    for d in train_data
]
y_train = [d["label"] for d in train_data]

X_test = [
    [d["temperature"], d["current"], d["vibration"]]
    for d in test_data
]
y_test = [d["label"] for d in test_data]

model = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Synthetic dataset evaluation")
print("----------------------------")
print(f"Training runs: {sorted(train_runs)}")
print(f"Test runs    : {sorted(test_runs)}")
print(f"Training samples: {len(train_data)}")
print(f"Test samples    : {len(test_data)}")
print()
print(f"Accuracy : {accuracy_score(y_test, predictions):.3f}")
print(f"Precision: {precision_score(y_test, predictions, zero_division=0):.3f}")
print(f"Recall   : {recall_score(y_test, predictions, zero_division=0):.3f}")
print(f"F1 Score : {f1_score(y_test, predictions, zero_division=0):.3f}")

joblib.dump(model, MODEL_FILE)

print()
print(f"Saved model to {MODEL_FILE}")
