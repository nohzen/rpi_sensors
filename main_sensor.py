import time, datetime, csv


mode = "office" # "office"

if mode == "home":
    csv_path = "data_home.csv"

    from mod_co2_mh_z19 import Co2SensorMhZ19
    from mod_thermometer_adt7410 import adt7410_read
elif mode == "office":
    csv_path = "data_office.csv"

    from mod_co2_mh_z19 import Co2SensorMhZ19
    from mod_thermometer_sht31 import HumidityTemperatureSensorSht31


# Write header
if False:
    with open(csv_path, 'a') as file:
        csv_writer = csv.writer(file)
        # csv_writer.writerow(["datetime",
        #                      "sht31_temperature", "sht31_humidity",
        #                      "adt7410_temperature",
        #                      "mhz19_1_co2", "mhz19_1_temperature",
        #                      "mhz19_2_co2", "mhz19_2_temperature"])
        if mode == "home":
            csv_writer.writerow(["datetime",
                                "adt7410_temperature",
                                "mhz19_co2", "mhz19_temperature"])
        elif mode == "office":
            csv_writer.writerow(["datetime",
                                "sht31_temperature", "sht31_humidity",
                                "mhz19_co2", "mhz19_temperature"])
        else:
            raise ValueError()


sht31_sensor = HumidityTemperatureSensorSht31()
co2_sensor = Co2SensorMhZ19(serial_device="/dev/ttyS0", abc=False)
# co2_sensor = Co2SensorMhZ19(serial_device="/dev/ttyAMA1", abc=False)

def main():
    now = datetime.datetime.now()

    if mode == "home":
        adt7410_temperature = adt7410_read()
        mhz19_co2, mhz19_temperature = co2_sensor.readall()
        with open(csv_path, 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([now, adt7410_temperature, mhz19_co2, mhz19_temperature])
    elif mode == "office":
        sht31_temperature, sht31_humidity = sht31_sensor.read()
        mhz19_co2, mhz19_temperature = co2_sensor.readall()
        # print(mhz19_co2, sht31_temperature, sht31_humidity)
        with open(csv_path, 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([now, sht31_temperature, sht31_humidity, mhz19_co2, mhz19_temperature])


while True:
    main()
    time.sleep(60.0)
