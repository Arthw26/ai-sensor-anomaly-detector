#include <stdio.h>
#include <time.h>

#include "../embedded/src/features.h"

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
    const int iterations = 1000000;

    struct timespec start;
    struct timespec end;

    clock_gettime(CLOCK_MONOTONIC, &start);

    float checksum = 0.0f;

    for (int i = 0; i < iterations; i++) {
        extract_features(&window, features);
        checksum += features[0];
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    long long elapsed =
        (long long)(end.tv_sec - start.tv_sec) * 1000000000LL +
        (end.tv_nsec - start.tv_nsec);

    printf("C Feature Extraction Benchmark\n");
    printf("------------------------------\n");
    printf("Iterations : %d\n", iterations);
    printf("Total time : %lld ns\n", elapsed);
    printf("Average    : %.2f ns\n",
           (double)elapsed / iterations);
    printf("Checksum   : %.2f\n", checksum);

    return 0;
}
