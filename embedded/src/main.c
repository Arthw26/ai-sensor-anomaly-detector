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

        if (sample >= 300) {
            break;
        }

        k_sleep(K_NO_WAIT);
    }

    return 0;
}
