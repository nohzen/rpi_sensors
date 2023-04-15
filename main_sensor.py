import os
import time, datetime
import csv
from co2_mh_z19 import Co2SensorMhZ19
from thermometer_adt7410 import adt7410_read
from thermometer_sht31 import HumidityTemperatureSensorSht31


sht31_sensor = HumidityTemperatureSensorSht31()
co2_sensor = Co2SensorMhZ19(serial_device="/dev/ttyS0", abc=False)


def write_header(csv_path, place):
    with open(csv_path, 'a') as file:
        csv_writer = csv.writer(file)
        # csv_writer.writerow(["datetime",
        #                      "sht31_temperature", "sht31_humidity",
        #                      "adt7410_temperature",
        #                      "mhz19_1_co2", "mhz19_1_temperature",
        #                      "mhz19_2_co2", "mhz19_2_temperature"])
        if place == "home":
            csv_writer.writerow(["datetime",
                                "adt7410_temperature",
                                "mhz19_co2", "mhz19_temperature"])
        elif place == "office":
            csv_writer.writerow(["datetime",
                                "sht31_temperature", "sht31_humidity",
                                "mhz19_co2", "mhz19_temperature"])
        else:
            raise NotImplementedError()


def read_sensor(csv_path, place):
    now = datetime.datetime.now()

    if place == "home":
        adt7410_temperature = adt7410_read()
        mhz19_co2, mhz19_temperature = co2_sensor.readall()
        with open(csv_path, 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([now, adt7410_temperature, mhz19_co2, mhz19_temperature])
    elif place == "office":
        sht31_temperature, sht31_humidity = sht31_sensor.read()
        mhz19_co2, mhz19_temperature = co2_sensor.readall()
        # print(mhz19_co2, sht31_temperature, sht31_humidity)
        with open(csv_path, 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([now, sht31_temperature, sht31_humidity, mhz19_co2, mhz19_temperature])
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default="./datas/data.csv",
                        help="Path to csv file")
    parser.add_argument("--place", default="office", choices=["office", "home"],
                        help="place to use (determine sensors)")
    args = parser.parse_args()

    csv_path = args.csv_path
    place = args.place

    if not os.path.isfile(csv_path):
        write_header(csv_path, place)

    while True:
        read_sensor(csv_path, place)
        time.sleep(60.0)
