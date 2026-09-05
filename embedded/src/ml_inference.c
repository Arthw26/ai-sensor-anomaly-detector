#include "ml_inference.h"

int anomaly_predict(float temperature, float current, float vibration)
{
    if (temperature <= 26.51f) {
        if (current <= 5.405f) {
            if (vibration <= 1.260f) {
                return 0;
            }

            return 1;
        }

        return 1;
    }

    return 1;
}

int anomaly_predict_features(const float features[FEATURE_COUNT])
{
    /*
     * Feature-based reference classifier.
     *
     * Uses the strongest learned features from the experimental
     * Random Forest: temperature max, temperature mean,
     * current max, and vibration peak-to-peak.
     */
    if (features[3] > 26.51f) {
        return 1;
    }

    if (features[7] > 5.405f) {
        return 1;
    }

    if (features[10] > 0.60f) {
        return 1;
    }

    if (features[0] > 26.05f) {
        return 1;
    }

    return 0;
}
