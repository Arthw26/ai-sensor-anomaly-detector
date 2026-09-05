# Performance Benchmark

## Embedded Functional Evaluation

The Zephyr `native_sim` application was evaluated over 300 virtual sensor samples with randomized fault windows.

| Metric | Result |
|---|---:|
| Samples | 300 |
| Accuracy | 1.000 |
| Precision | 1.000 |
| Recall | 1.000 |
| F1 Score | 1.000 |
| False positives | 0 |
| False negatives | 0 |

The test included independent temperature, current, and vibration fault windows.

## Feature-Based Renode Evaluation

The feature extraction and feature-based classifier were evaluated on Zephyr's `riscv32_virtual` target running under Renode.

The detector processes non-overlapping windows of 10 sensor samples.

| Metric | Result |
|---|---:|
| Windows evaluated | 30 |
| Window size | 10 samples |
| Accuracy | 1.000 |
| Precision | 1.000 |
| Recall | 1.000 |
| F1 Score | 1.000 |
| False positives | 0 |
| False negatives | 0 |
| True positives | 6 |
| True negatives | 24 |

All six windows overlapping the simulated temperature, current, and vibration fault periods were detected, while all 24 normal windows were classified correctly.

This is a deterministic simulation result and should not be interpreted as evidence of 100% performance on unseen real-world data.

## Renode RISC-V Evaluation

The raw-sensor embedded Decision Tree was also evaluated over 300 samples on the `riscv32_virtual` target under Renode.

| Metric | Result |
|---|---:|
| Samples | 300 |
| Accuracy | 0.997 |
| Precision | 1.000 |
| Recall | 0.971 |
| F1 Score | 0.986 |
| False positives | 0 |
| False negatives | 1 |
| True positives | 34 |
| True negatives | 265 |

The single false negative occurred during the simulated vibration fault window.

## Host ML Inference Benchmark

The C inference function was benchmarked on the WSL/Linux host.

- Optimization: `-O2`
- Total inferences: 40,000,000
- Elapsed time: 82,164,733 ns
- Average inference: 2.05 ns
- Checksum: 30,000,000

This latency is a **host benchmark**, not an MCU latency measurement.

## Feature Extraction Benchmark

The 13-feature C feature extractor was benchmarked using one million 10-sample windows.

| Metric | Result |
|---|---:|
| Iterations | 1,000,000 |
| Total time | 98,639,099 ns |
| Average | 98.64 ns/window |
| Checksum | 25,331,472 |

The equivalent Python reference implementation measured approximately 17.03 microseconds per window on the same host environment.

These are host measurements and do not represent MCU execution time.

## Complete Feature Pipeline Benchmark

The feature extraction and feature-based anomaly classification pipeline was benchmarked together on the host.

| Metric | Result |
|---|---:|
| Iterations | 1,000,000 |
| Total time | 128,927,997 ns |
| Average | 128.93 ns/window |

This benchmark includes feature extraction and embedded anomaly classification. It is a host-C benchmark and does not represent the latency of a specific microcontroller.

## RISC-V Firmware Footprint

The Zephyr firmware was built for the `riscv32_virtual` Renode target.

| Resource | Before feature extraction | With feature extraction |
|---|---:|---:|
| ROM | 31,888 B | 35,008 B |
| RAM | 4,272 B | 4,272 B |

The current feature-enabled firmware therefore uses 3,120 additional bytes of ROM compared with the earlier baseline build, while RAM usage remains unchanged.

The feature window uses a fixed 10-sample buffer, making its memory requirement deterministic.

## ML Model Comparison

Two ML approaches were evaluated on the generated sensor dataset.

| Model | Input | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|
| Baseline Decision Tree | 3 raw sensors | 99.8% | 100% | 98.6% | **99.3%** |
| Feature-based Random Forest | 13 window features | 99.7% | 100% | 98.4% | **99.2%** |

Five-fold cross-validation of the feature-based Random Forest produced an average F1 score of approximately 98.9%.

The feature-based Random Forest provides richer signal representation, but its performance does not justify replacing the smaller embedded Decision Tree for this dataset. The compact Decision Tree therefore remains the primary raw-sensor ML inference model.

The embedded feature-based classifier is a compact reference implementation using selected features and manually derived thresholds informed by the experimental feature-model analysis. It is not an embedded export of the Random Forest.

## Native_sim Resource Footprint

Earlier native_sim measurements for the whole Zephyr ELF were:

| Section | Bytes |
|---|---:|
| Text | 12,650 |
| Data | 124 |
| BSS | 4,515 |
| Total | 17,289 |

## Standalone C Inference Benchmark

| Section | Bytes |
|---|---:|
| Text | 2,428 |
| Data | 624 |
| BSS | 8 |
| Total | 3,060 |

The standalone binary size represents the benchmark executable and should not be interpreted as the size of the ML model alone.

## Timing Limitation

Zephyr timing instrumentation on `native_sim` returned zero-duration measurements for the very small inference function. Those results were not used as latency measurements.

The project therefore reports reproducible host-C benchmarks while avoiding misleading claims about actual microcontroller execution time.

Actual MCU latency would require deployment to a physical target or a simulator capable of providing a sufficiently meaningful cycle-accurate execution model.
