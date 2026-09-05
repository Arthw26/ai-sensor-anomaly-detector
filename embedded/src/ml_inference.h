#ifndef ML_INFERENCE_H
#define ML_INFERENCE_H

#include "features.h"

int anomaly_predict(float temperature, float current, float vibration);

int anomaly_predict_features(const float features[FEATURE_COUNT]);

#endif
