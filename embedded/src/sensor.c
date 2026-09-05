#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#include "sensor.h"

static unsigned int random_state = 0x12345678u;

static unsigned int sensor_random(void)
{
    random_state ^= random_state << 13;
    random_state ^= random_state >> 17;
    random_state ^= random_state << 5;

    return random_state;
}

static int temp_start;
static int current_start;
static int vibration_start;
static bool initialized;

static void initialize_fault_windows(void)
{
    if (initialized) {
        return;
    }

    temp_start = 20 + (sensor_random() % 61);
    current_start = 100 + (sensor_random() % 81);
    vibration_start = 200 + (sensor_random() % 61);

    initialized = true;

    printk("FAULT_WINDOWS,temp=%d,current=%d,vibration=%d\n",
           temp_start, current_start, vibration_start);
}

static int sensor_read_temperature(int sample)
{
    int noise = (int)(sensor_random() % 31) - 15;

    if (sample >= temp_start && sample < temp_start + 20) {
        return 280 + noise;
    }

    return 250 + noise;
}

static int sensor_read_current(int sample)
{
    int noise = (int)(sensor_random() % 81) - 40;

    if (sample >= current_start && sample < current_start + 10) {
        return 580 + noise;
    }

    return 500 + noise;
}

static int sensor_read_vibration(int sample)
{
    int noise = (int)(sensor_random() % 51) - 25;

    if (sample >= vibration_start && sample < vibration_start + 5) {
        return 140 + noise;
    }

    return 100 + noise;
}

struct sensor_data sensor_task(int sample)
{
    initialize_fault_windows();

    struct sensor_data data;

    int temperature = sensor_read_temperature(sample);
    int current = sensor_read_current(sample);
    int vibration = sensor_read_vibration(sample);

    data.temperature = temperature / 10.0f;
    data.current = current / 100.0f;
    data.vibration = vibration / 100.0f;

    return data;
}
