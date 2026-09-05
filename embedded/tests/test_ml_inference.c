#include <assert.h>
#include <stdio.h>

#include "../src/ml_inference.h"

int main(void)
{
    /* Raw-sensor Decision Tree tests */

    assert(anomaly_predict(25.0f, 5.0f, 1.0f) == 0);

    assert(anomaly_predict(29.0f, 5.0f, 1.0f) == 1);

    assert(anomaly_predict(25.0f, 6.0f, 1.0f) == 1);

    assert(anomaly_predict(25.0f, 5.0f, 1.5f) == 1);

    /* Feature-based classifier tests */

    float normal[FEATURE_COUNT] = {
        25.0f, 0.04f, 0.7f, 25.4f,
        5.0f, 0.02f, 0.4f, 5.2f,
        1.0f, 0.01f, 0.4f, 1.2f, 1.01f
    };

    assert(anomaly_predict_features(normal) == 0);

    float high_temperature[FEATURE_COUNT] = {
        26.8f, 0.04f, 0.7f, 27.2f,
        5.0f, 0.02f, 0.4f, 5.2f,
        1.0f, 0.01f, 0.4f, 1.2f, 1.01f
    };

    assert(anomaly_predict_features(high_temperature) == 1);

    float high_current[FEATURE_COUNT] = {
        25.0f, 0.04f, 0.7f, 25.4f,
        5.8f, 0.02f, 0.4f, 5.7f,
        1.0f, 0.01f, 0.4f, 1.2f, 1.01f
    };

    assert(anomaly_predict_features(high_current) == 1);

    float high_vibration_variation[FEATURE_COUNT] = {
        25.0f, 0.04f, 0.7f, 25.4f,
        5.0f, 0.02f, 0.4f, 5.2f,
        1.0f, 0.02f, 0.8f, 1.4f, 1.05f
    };

    assert(anomaly_predict_features(high_vibration_variation) == 1);

    printf("All ML inference tests passed.\n");
    return 0;
}
