import csv

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate

from feature_extraction import extract_features


DATASET = "python/data/synthetic_sensor_data.csv"
WINDOW_SIZE = 10


def load_runs():
    runs = {}

    with open(DATASET, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            run = int(row["run"])

            runs.setdefault(run, []).append({
                "temperature": float(row["temperature"]),
                "current": float(row["current"]),
                "vibration": float(row["vibration"]),
                "label": int(row["label"]),
            })

    return runs


def build_windows(samples):
    features = []
    labels = []

    for start in range(len(samples) - WINDOW_SIZE + 1):
        window = samples[start:start + WINDOW_SIZE]

        features.append(
            extract_features(
                [x["temperature"] for x in window],
                [x["current"] for x in window],
                [x["vibration"] for x in window],
            )
        )

        labels.append(int(any(x["label"] for x in window)))

    return features, labels


runs = load_runs()

X = []
y = []

for run in range(1, 9):
    features, labels = build_windows(runs[run])
    X.extend(features)
    y.extend(labels)

model = RandomForestClassifier(
    n_estimators=50,
    max_depth=5,
    random_state=42,
)

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)

scores = cross_validate(
    model,
    X,
    y,
    cv=cv,
    scoring=[
        "accuracy",
        "precision",
        "recall",
        "f1",
    ],
)

print("5-Fold Cross-Validation")
print("-----------------------")

for metric in ["accuracy", "precision", "recall", "f1"]:
    values = scores[f"test_{metric}"]
    print(
        f"{metric.capitalize():9s}: "
        f"{values.mean():.3f} +/- {values.std():.3f}"
    )
