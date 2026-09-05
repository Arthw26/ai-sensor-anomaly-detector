#include "features.h"

#include <math.h>

static float mean(const float *values)
{
    float sum = 0.0f;

    for (int i = 0; i < SENSOR_WINDOW_SIZE; i++) {
        sum += values[i];
    }

    return sum / SENSOR_WINDOW_SIZE;
}

static float variance(const float *values, float average)
{
    float sum = 0.0f;

    for (int i = 0; i < SENSOR_WINDOW_SIZE; i++) {
        float delta = values[i] - average;
        sum += delta * delta;
    }

    return sum / SENSOR_WINDOW_SIZE;
}

static float peak_to_peak(const float *values)
{
    float minimum = values[0];
    float maximum = values[0];

    for (int i = 1; i < SENSOR_WINDOW_SIZE; i++) {
        if (values[i] < minimum) {
            minimum = values[i];
        }

        if (values[i] > maximum) {
            maximum = values[i];
        }
    }

    return maximum - minimum;
}

static float maximum(const float *values)
{
    float result = values[0];

    for (int i = 1; i < SENSOR_WINDOW_SIZE; i++) {
        if (values[i] > result) {
            result = values[i];
        }
    }

    return result;
}

static float rms(const float *values)
{
    float sum = 0.0f;

    for (int i = 0; i < SENSOR_WINDOW_SIZE; i++) {
        sum += values[i] * values[i];
    }

    return sqrtf(sum / SENSOR_WINDOW_SIZE);
}

void extract_features(
    const struct sensor_window *window,
    float features[FEATURE_COUNT]
)
{
    float temp_mean = mean(window->temperature);
    float current_mean = mean(window->current);
    float vibration_mean = mean(window->vibration);

    features[0] = temp_mean;
    features[1] = variance(window->temperature, temp_mean);
    features[2] = peak_to_peak(window->temperature);
    features[3] = maximum(window->temperature);

    features[4] = current_mean;
    features[5] = variance(window->current, current_mean);
    features[6] = peak_to_peak(window->current);
    features[7] = maximum(window->current);

    features[8] = vibration_mean;
    features[9] = variance(window->vibration, vibration_mean);
    features[10] = peak_to_peak(window->vibration);
    features[11] = maximum(window->vibration);
    features[12] = rms(window->vibration);
}
