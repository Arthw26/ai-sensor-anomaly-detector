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
