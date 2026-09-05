#include <zephyr/kernel.h>
#include <zephyr/random/random.h>
#include <zephyr/sys/printk.h>

static int sensor_read_temperature(int sample)
{
    int noise = (int)(sys_rand32_get() % 11) - 5;

    if (sample >= 8 && sample <= 12) {
        return 350 + noise;
    }

    return 250 + noise;
}

static int sensor_read_current(int sample)
{
    int noise = (int)(sys_rand32_get() % 21) - 10;

    if ((sample >= 8 && sample <= 12) ||
        (sample >= 20 && sample <= 24)) {
        return 800 + noise;
    }

    return 500 + noise;
}

void sensor_task(void)
{
    static int sample = 0;
    sample++;

    int temperature = sensor_read_temperature(sample);
    int current = sensor_read_current(sample);

    printk("%d.%d,%d.%02d\n",
           temperature / 10,
           temperature % 10,
           current / 100,
           current % 100);
}
