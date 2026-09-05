import math


def mean(values):
    return sum(values) / len(values)


def variance(values):
    avg = mean(values)
    return sum((x - avg) ** 2 for x in values) / len(values)


def rms(values):
    return math.sqrt(sum(x * x for x in values) / len(values))


def peak_to_peak(values):
    return max(values) - min(values)


def maximum(values):
    return max(values)


def extract_features(temperature, current, vibration):
    return [
        mean(temperature),
        variance(temperature),
        peak_to_peak(temperature),
        maximum(temperature),
        mean(current),
        variance(current),
        peak_to_peak(current),
        maximum(current),
        mean(vibration),
        variance(vibration),
        peak_to_peak(vibration),
        maximum(vibration),
        rms(vibration),
    ]
