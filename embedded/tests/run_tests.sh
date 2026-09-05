#!/usr/bin/env bash
set -e

gcc -Wall -Wextra -Werror \
    embedded/tests/test_ml_inference.c \
    embedded/src/ml_inference.c \
    -o /tmp/test_ml_inference

/tmp/test_ml_inference

gcc -Wall -Wextra -Werror \
    embedded/tests/test_features.c \
    embedded/src/features.c \
    -lm \
    -o /tmp/test_features

/tmp/test_features

gcc -Wall -Wextra -Werror \
    embedded/tests/test_sensor_features.c \
    embedded/src/features.c \
    -lm \
    -o /tmp/test_sensor_features

/tmp/test_sensor_features
