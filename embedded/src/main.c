#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#include "ml_inference.h"

struct sensor_data {
    float temperature;
    float current;
    float vibration;
};

struct sensor_data sensor_task(int sample);

int main(void)
{
    int sample = 0;

    printk("AI Sensor Anomaly Detector\n");
    printk("Virtual embedded device starting...\n");

    while (1) {
        sample++;

        struct sensor_data data = sensor_task(sample);

        int anomaly = anomaly_predict(
            data.temperature,
            data.current,
            data.vibration
        );

        int temp = (int)(data.temperature * 100.0f);
        int current = (int)(data.current * 100.0f);
        int vibration = (int)(data.vibration * 100.0f);

        printk(
            "DATA,%d,%d.%02d,%d.%02d,%d.%02d,%d\n",
            sample,
            temp / 100, temp % 100,
            current / 100, current % 100,
            vibration / 100, vibration % 100,
            anomaly
        );

        if (sample >= 300) {
            break;
        }

        k_sleep(K_NO_WAIT);
    }

    return 0;
}
