#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

void sensor_task(void);

int main(void)
{
    int sample = 0;

    printk("AI Sensor Anomaly Detector\n");
    printk("Virtual embedded device starting...\n");

    while (1) {
        sample++;
        printk("DATA,%d,", sample);
        sensor_task();
        k_sleep(K_SECONDS(1));
    }

    return 0;
}
