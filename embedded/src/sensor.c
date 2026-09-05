#include <zephyr/kernel.h>
#include <zephyr/random/random.h>
#include <zephyr/sys/printk.h>

static int sensor_read_temperature(int sample)
{
    int noise = (int)(sys_rand32_get() % 21) - 10;

    if (sample >= 14 && sample <= 33) {
        return 290 + noise;
    }

    return 250 + noise;
}

static int sensor_read_current(int sample)
{
    int noise = (int)(sys_rand32_get() % 61) - 30;

    if (sample >= 40 && sample <= 49) {
        return 620 + noise;
    }

    return 500 + noise;
}

static int sensor_read_vibration(int sample)
{
    int noise = (int)(sys_rand32_get() % 41) - 20;

    if (sample >= 30 && sample <= 34) {
        return 160 + noise;
    }

    return 100 + noise;
}

void sensor_task(void)
{
    static int sample = 0;
    sample++;

    int temperature = sensor_read_temperature(sample);
    int current = sensor_read_current(sample);
    int vibration = sensor_read_vibration(sample);

    printk("%d.%d,%d.%02d,%d.%02d\n",
           temperature / 10,
           temperature % 10,
           current / 100,
           current % 100,
           vibration / 100,
           vibration % 100);
}
