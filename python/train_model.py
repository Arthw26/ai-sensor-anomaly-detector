import csv
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

data = []

with open("python/data/training_data.csv", "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        data.append({
            "temperature": float(row["temperature"]),
            "current": float(row["current"]),
            "label": int(row["label"])
        })

X = [[d["temperature"], d["current"]] for d in data]
y = [d["label"] for d in data]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

model = DecisionTreeClassifier(
    max_depth=2,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Model evaluation")
print("----------------")
print(f"Accuracy : {accuracy_score(y_test, predictions):.3f}")
print(f"Precision: {precision_score(y_test, predictions, zero_division=0):.3f}")
print(f"Recall   : {recall_score(y_test, predictions, zero_division=0):.3f}")
print(f"F1 Score : {f1_score(y_test, predictions, zero_division=0):.3f}")

joblib.dump(model, "python/models/anomaly_detector.joblib")

print()
print("Saved model to python/models/anomaly_detector.joblib")
