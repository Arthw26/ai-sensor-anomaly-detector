import time

from feature_extraction import extract_features


temperature = [25.0, 25.2, 24.8, 25.1, 25.4, 24.9, 25.0, 25.3, 24.7, 25.1]
current = [5.0, 5.1, 4.9, 5.2, 5.0, 4.8, 5.1, 5.0, 4.9, 5.2]
vibration = [1.0, 1.1, 0.9, 1.0, 1.2, 0.8, 1.0, 1.1, 0.9, 1.0]

iterations = 1_000_000

start = time.perf_counter_ns()

checksum = 0.0

for _ in range(iterations):
    features = extract_features(
        temperature,
        current,
        vibration,
    )
    checksum += features[0]

elapsed = time.perf_counter_ns() - start

print("Python Feature Extraction Benchmark")
print("------------------------------------")
print(f"Iterations : {iterations:,}")
print(f"Total time : {elapsed:,} ns")
print(f"Average    : {elapsed / iterations:.2f} ns")
print(f"Checksum   : {checksum:.2f}")
