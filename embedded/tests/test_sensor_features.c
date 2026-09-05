#include <assert.h>
#include <math.h>
#include <stdio.h>

#include "../src/features.h"

int main(void)
{
    struct sensor_window window = {0};

    for (int i = 0; i < SENSOR_WINDOW_SIZE; i++) {
        window.temperature[i] = 25.0f;
        window.current[i] = 5.0f;
        window.vibration[i] = 1.0f;
    }

    float features[FEATURE_COUNT];

    extract_features(&window, features);

    /* Constant signals should have zero variance and zero peak-to-peak. */
    assert(fabsf(features[0] - 25.0f) < 0.001f);
    assert(fabsf(features[1]) < 0.001f);
    assert(fabsf(features[2]) < 0.001f);
    assert(fabsf(features[3] - 25.0f) < 0.001f);

    assert(fabsf(features[4] - 5.0f) < 0.001f);
    assert(fabsf(features[5]) < 0.001f);
    assert(fabsf(features[6]) < 0.001f);
    assert(fabsf(features[7] - 5.0f) < 0.001f);

    assert(fabsf(features[8] - 1.0f) < 0.001f);
    assert(fabsf(features[9]) < 0.001f);
    assert(fabsf(features[10]) < 0.001f);
    assert(fabsf(features[11] - 1.0f) < 0.001f);
    assert(fabsf(features[12] - 1.0f) < 0.001f);

    printf("Sensor-to-feature integration tests passed.\n");

    return 0;
}
