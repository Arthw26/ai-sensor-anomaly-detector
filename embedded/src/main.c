#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#include "features.h"
#include "ml_inference.h"
#include "sensor.h"


int main(void)
{
    int sample = 0;
    struct sensor_window window = {0};
    float features[FEATURE_COUNT];

    printk("AI Sensor Anomaly Detector\n");
    printk("Virtual embedded device starting...\n");

    while (1) {
        sample++;

        struct sensor_data data = sensor_task(sample);

        int window_index = (sample - 1) % SENSOR_WINDOW_SIZE;

        window.temperature[window_index] = data.temperature;
        window.current[window_index] = data.current;
        window.vibration[window_index] = data.vibration;

        int anomaly = anomaly_predict(
            data.temperature,
            data.current,
            data.vibration
        );

        if (sample >= SENSOR_WINDOW_SIZE &&
            window_index == SENSOR_WINDOW_SIZE - 1) {
            extract_features(&window, features);

            int temp_mean = (int)(features[0] * 100.0f);
            int temp_max = (int)(features[3] * 100.0f);
            int current_mean = (int)(features[4] * 100.0f);
            int current_max = (int)(features[7] * 100.0f);
            int vibration_mean = (int)(features[8] * 100.0f);
            int vibration_max = (int)(features[11] * 100.0f);
            int vibration_rms = (int)(features[12] * 100.0f);

            printk(
                "FEATURES,temp_mean=%d.%02d,temp_max=%d.%02d,current_mean=%d.%02d,current_max=%d.%02d,vibration_mean=%d.%02d,vibration_max=%d.%02d,vibration_rms=%d.%02d\n",
                temp_mean / 100, temp_mean % 100,
                temp_max / 100, temp_max % 100,
                current_mean / 100, current_mean % 100,
                current_max / 100, current_max % 100,
                vibration_mean / 100, vibration_mean % 100,
                vibration_max / 100, vibration_max % 100,
                vibration_rms / 100, vibration_rms % 100
            );
        }

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
