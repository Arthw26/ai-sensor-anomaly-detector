#include <stdio.h>
#include <time.h>

#include "../embedded/src/ml_inference.h"

int main(void)
{
    const int iterations = 10000000;
    volatile int result = 0;

    struct timespec start;
    struct timespec end;

    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < iterations; i++) {
        result += anomaly_predict(25.0f, 5.0f, 1.0f);
        result += anomaly_predict(29.0f, 5.0f, 1.0f);
        result += anomaly_predict(25.0f, 6.0f, 1.0f);
        result += anomaly_predict(25.0f, 5.0f, 1.5f);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    long long elapsed_ns =
        (long long)(end.tv_sec - start.tv_sec) * 1000000000LL +
        (end.tv_nsec - start.tv_nsec);

    long long total_inferences = (long long)iterations * 4;
    double avg_ns = (double)elapsed_ns / total_inferences;

    printf("ML inference benchmark\n");
    printf("----------------------\n");
    printf("Total inferences: %lld\n", total_inferences);
    printf("Elapsed time: %lld ns\n", elapsed_ns);
    printf("Average inference: %.2f ns\n", avg_ns);
    printf("Checksum: %d\n", result);

    return 0;
}
