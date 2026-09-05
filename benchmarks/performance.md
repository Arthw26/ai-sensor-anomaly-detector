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

## Host ML Inference Benchmark

The C inference function was benchmarked on the WSL/Linux host.

- Optimization: `-O2`
- Total inferences: 40,000,000
- Elapsed time: 82,164,733 ns
- Average inference: 2.05 ns
- Checksum: 30,000,000

This latency is a **host benchmark**, not an MCU latency measurement.

## Native_sim Resource Footprint

Whole Zephyr `native_sim` ELF:

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

Zephyr timing instrumentation on `native_sim` returned zero-duration measurements for this very small inference function. Those results were not used as latency measurements.

The project therefore reports the reproducible host benchmark while avoiding a misleading `native_sim` latency claim.
