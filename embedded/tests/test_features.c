#include <assert.h>
#include <math.h>
#include <stdio.h>

#include "../src/features.h"

int main(void)
{
    struct sensor_window window = {
        .temperature = {
            25.0f, 25.2f, 24.8f, 25.1f, 25.4f,
            24.9f, 25.0f, 25.3f, 24.7f, 25.1f
        },
        .current = {
            5.0f, 5.1f, 4.9f, 5.2f, 5.0f,
            4.8f, 5.1f, 5.0f, 4.9f, 5.2f
        },
        .vibration = {
            1.0f, 1.1f, 0.9f, 1.0f, 1.2f,
            0.8f, 1.0f, 1.1f, 0.9f, 1.0f
        }
    };

    float features[FEATURE_COUNT];

    extract_features(&window, features);

    /* Temperature */
    assert(fabsf(features[0] - 25.05f) < 0.001f);
    assert(fabsf(features[1] - 0.0425f) < 0.001f);
    assert(fabsf(features[2] - 0.7f) < 0.001f);
    assert(fabsf(features[3] - 25.4f) < 0.001f);

    /* Current */
    assert(fabsf(features[4] - 5.02f) < 0.001f);
    assert(fabsf(features[5] - 0.0156f) < 0.001f);
    assert(fabsf(features[6] - 0.4f) < 0.001f);
    assert(fabsf(features[7] - 5.2f) < 0.001f);

    /* Vibration */
    assert(fabsf(features[8] - 1.0f) < 0.001f);
    assert(fabsf(features[9] - 0.012f) < 0.001f);
    assert(fabsf(features[10] - 0.4f) < 0.001f);
    assert(fabsf(features[11] - 1.2f) < 0.001f);
    assert(fabsf(features[12] - 1.00599f) < 0.001f);

    printf("C feature extraction tests passed.\n");

    return 0;
}
