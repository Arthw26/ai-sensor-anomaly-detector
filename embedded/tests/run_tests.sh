#!/usr/bin/env bash
set -e

gcc -Wall -Wextra -Werror \
    embedded/tests/test_ml_inference.c \
    embedded/src/ml_inference.c \
    -o /tmp/test_ml_inference

/tmp/test_ml_inference
