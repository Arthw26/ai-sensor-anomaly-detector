# Renode Embedded Evaluation

## Configuration

- Target: Zephyr `riscv32_virtual`
- Emulator: Renode 1.16.1
- Samples evaluated: 300
- Fault types: temperature, current, vibration

## Results

| Metric | Score |
|---|---:|
| Accuracy | 0.997 |
| Precision | 1.000 |
| Recall | 0.971 |
| F1 Score | 0.986 |
| False positives | 0 |
| False negatives | 1 |
| True positives | 34 |
| True negatives | 265 |

## Fault Windows

- Temperature: samples 50-69
- Current: samples 120-129
- Vibration: samples 222-226

## Failure Analysis

One injected anomaly was missed during the Renode evaluation.

The missed detection occurred because the generated vibration-fault signal can overlap the normal operating distribution. The embedded decision tree therefore classified one anomalous sample as normal.

This demonstrates that the embedded inference implementation reproduces the trained model's behavior while also exposing limitations caused by overlapping sensor distributions.

## Conclusion

The complete software pipeline was successfully executed on a virtual RISC-V embedded platform:

Virtual sensors -> Zephyr RTOS -> C ML inference -> Renode -> UART telemetry

The system achieved 0.997 accuracy and 1.000 precision during the Renode evaluation, with one false negative and no false positives.
