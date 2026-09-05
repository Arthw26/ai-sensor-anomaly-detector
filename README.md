# AI Sensor Anomaly Detector

AI-powered anomaly detection running on a virtual embedded device using **Zephyr RTOS**, **C**, **Python**, and **Renode**.

## Overview

This project simulates an industrial embedded device with three virtual sensors:

- Temperature
- Current
- Vibration

Synthetic sensor data is used to train a lightweight decision-tree anomaly detector. The learned decision rules are then implemented directly in C and executed as embedded firmware.

The firmware is tested first with Zephyr `native_sim` and then on a virtual RISC-V embedded platform using Renode.

## Architecture

```text
Virtual Sensors
      |
      v
Sensor Data
      |
      v
Feature Values
      |
      v
Decision Tree Inference
      |
      v
Normal / Anomaly
      |
      v
UART Telemetry
      |
      v
Renode Evaluation

## Machine Learning

The model uses three input features:

- Temperature
- Current
- Vibration

A `DecisionTreeClassifier` with maximum depth 3 is trained using synthetic data.

The dataset contains:

- 3,000 samples
- 10 independent simulation runs
- 2,400 training samples
- 600 test samples
- 2,650 normal samples
- 350 anomaly samples

Training uses runs 1-8 and evaluation uses previously unseen runs 9-10.

### Model performance

| Metric | Score |
|---|---:|
| Accuracy | 0.998 |
| Precision | 1.000 |
| Recall | 0.986 |
| F1 Score | 0.993 |

The model contains only 7 decision-tree nodes with a maximum depth of 3, making it suitable for lightweight embedded inference.

## Embedded Implementation

The trained decision rules were translated into a small C inference function.

Example learned thresholds:

```text
Temperature > 26.51 C -> anomaly
Current > 5.405 A -> anomaly
Vibration > 1.260 g -> anomaly
Otherwise -> normal

The embedded implementation is tested independently with C unit tests covering:

- Normal operation
- Temperature anomaly
- Current anomaly
- Vibration anomaly

## Zephyr RTOS

The firmware runs on Zephyr RTOS.

Supported simulation targets:

- `native_sim`
- `riscv32_virtual`

The `native_sim` target allows the embedded application to run as a Linux executable without physical hardware.

## Renode

The RISC-V version runs on the Zephyr `riscv32_virtual` target inside Renode.

Renode executes the actual Zephyr firmware ELF and provides the virtual CPU and peripherals required by the application.

Automated evaluation parses the firmware UART telemetry and compares embedded predictions against the known injected fault windows.

### Renode results

| Metric | Score |
|---|---:|
| Samples evaluated | 300 |
| Accuracy | 0.997 |
| Precision | 1.000 |
| Recall | 0.971 |
| F1 Score | 0.986 |
| False positives | 0 |
| False negatives | 1 |

The single missed anomaly occurs because one generated vibration fault overlaps the normal sensor distribution.

Rather than hiding this failure, the project documents it as a limitation of the available sensor signal.

## Performance

### Host C inference benchmark

The C inference function was benchmarked on the WSL/Linux host:

- Total inferences: 40,000,000
- Optimization: `-O2`
- Average inference time: 2.05 ns

This is a **host benchmark**, not an MCU latency measurement.

### Native_sim footprint

Whole Zephyr `native_sim` ELF:

| Section | Bytes |
|---|---:|
| Text | 12,650 |
| Data | 124 |
| BSS | 4,515 |
| Total | 17,289 |

The standalone benchmark executable is approximately 3.0 KiB. This should not be interpreted as the ML model size alone.

## Repository Structure

The repository is organized into Python ML development, embedded firmware, simulation, Renode configuration, and benchmarking.

## Running the Project

### 1. Run the C unit tests

`./embedded/tests/run_tests.sh`

### 2. Build for Zephyr native_sim

`cd ~/zephyrproject && west build -b native_sim ~/ai_sensor_anomaly_detector/embedded`

Run the firmware:

`west build -t run`

### 3. Build the RISC-V virtual target

`cd ~/zephyrproject && west build -b riscv32_virtual ~/ai_sensor_anomaly_detector/embedded -d ~/ai_sensor_anomaly_detector/build_riscv`

### 4. Run Renode

`cd ~/ai_sensor_anomaly_detector && renode --plain --disable-xwt renode/anomaly_detector.resc`

### 5. Run automated Renode evaluation

`python3 benchmarks/evaluate_renode.py`

## Limitations

This project intentionally uses virtual sensors and simulated hardware.

The reported 2.05 ns inference measurement is a host/Linux benchmark and should not be treated as embedded CPU latency.

The anomaly detector has one documented false negative during Renode evaluation because the synthetic vibration anomaly distribution overlaps normal operation.

A production system would require real sensor data, calibration, noise characterization, hardware-specific timing measurements, and additional fault scenarios.

## Future Improvements

- More realistic sensor noise and drift
- Additional fault types
- Feature engineering and signal-processing features
- Quantized or integer-only inference
- Hardware-specific latency and RAM measurements
- Continuous integration
- Automated dataset/model regeneration
- More extensive Renode regression tests

## Technologies

- C / C++
- Python
- scikit-learn
- Zephyr RTOS
- Renode
- RISC-V
- WSL2 / Ubuntu
- Git / GitHub

## Status

**Portfolio project — functional end-to-end prototype.**
