#include <assert.h>
#include <stdio.h>

#include "../src/ml_inference.h"

int main(void)
{
    /* Normal operating point */
    assert(anomaly_predict(25.0f, 5.0f, 1.0f) == 0);

    /* Temperature anomaly */
    assert(anomaly_predict(29.0f, 5.0f, 1.0f) == 1);

    /* Current anomaly */
    assert(anomaly_predict(25.0f, 6.0f, 1.0f) == 1);

    /* Vibration anomaly */
    assert(anomaly_predict(25.0f, 5.0f, 1.5f) == 1);

    printf("All ML inference tests passed.\n");
    return 0;
}
