#ifndef FEATURES_H
#define FEATURES_H

#define SENSOR_WINDOW_SIZE 10
#define FEATURE_COUNT 13

struct sensor_window {
    float temperature[SENSOR_WINDOW_SIZE];
    float current[SENSOR_WINDOW_SIZE];
    float vibration[SENSOR_WINDOW_SIZE];
};

void extract_features(
    const struct sensor_window *window,
    float features[FEATURE_COUNT]
);

#endif
