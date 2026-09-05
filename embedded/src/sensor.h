#ifndef SENSOR_H
#define SENSOR_H

struct sensor_data {
    float temperature;
    float current;
    float vibration;
};

struct sensor_data sensor_task(int sample);

#endif
