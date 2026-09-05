# ML Baseline Benchmark

## Model

Decision Tree Classifier

- Max depth: 3
- Features: temperature, current, vibration
- Random seed: 42

## Dataset

- Total samples: 3,000
- Runs: 10
- Training runs: 1-8
- Test runs: 9-10
- Training samples: 2,400
- Test samples: 600

## Results

| Metric | Score |
|---|---:|
| Accuracy | 0.998 |
| Precision | 1.000 |
| Recall | 0.986 |
| F1 Score | 0.993 |

## Failure Analysis

- Missed anomalies: 1
- False positives: 0

The missed anomaly was:

- Run: 10
- Sample: 253
- Temperature: 23.6 C
- Current: 4.83 A
- Vibration: 1.26 g
- Actual label: anomaly
- Predicted label: normal
- Anomaly probability: 0.0052

The failure occurs because the sensor values overlap the normal operating distribution. This demonstrates a limitation of the available sensor information rather than simply a model threshold error.

## Feature Importance

- Temperature: 54.1%
- Current: 30.0%
- Vibration: 15.9%

## Decision Rules

The trained tree learned approximately:

- Temperature > 26.51 C -> anomaly
- Otherwise, current > 5.40 A -> anomaly
- Otherwise, vibration > 1.26 g -> anomaly
- Otherwise -> normal
