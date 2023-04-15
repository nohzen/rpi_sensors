"""CO2 sensor MH-Z19
Reference: https://github.com/UedaTakeyuki/mh-z19

MH-Z19 -- RaspberryPi
==========================
GND    -- GND
Vin    -- 5V（Pin2 or Pin4）
Tx     -- UART RXD (GPIO 15)
Rx     -- UART TXD (GPIO 14)
* RXD, TXD can be change when serial device is not /dev/ttyS0
"""
import mh_z19


class Co2SensorMhZ19:
    def __init__(self, serial_device="/dev/ttyS0", abc=True):
        """
        serial_device  : TXD, RXD
        ====
        "/dev/ttyS0"   : 14,  15
        "/dev/ttyAMA0" : 14,  15
        "/dev/ttyAMA1" :  0,   1
        "/dev/ttyAMA2" :  4,   5
        "/dev/ttyAMA3" :  8,   9
        "/dev/ttyAMA4" : 12,  13
        """
        self.serial_device = serial_device
        mh_z19.set_serialdevice(self.serial_device)
        if abc:
            mh_z19.abc_on(serial_console_untouched=True)
        else:
            mh_z19.abc_off(serial_console_untouched=True)

    def read_CO2(self):
        mh_z19.set_serialdevice(self.serial_device)
        data_dict = mh_z19.read(serial_console_untouched=True)
        return data_dict['co2']

    def readall(self):
        mh_z19.set_serialdevice(self.serial_device)
        data_dict = mh_z19.read_all(serial_console_untouched=True)
        co2_ppm = data_dict['co2']
        temperature = data_dict['temperature']
        return co2_ppm, temperature # [ppm], [degree Celsius]


if __name__ == '__main__':
    from time import sleep
    import datetime

    co2_sensor1 = Co2SensorMhZ19(serial_device="/dev/ttyS0", abc=False)
    # co2_sensor2 = Co2SensorMhZ19(serial_device="/dev/ttyAMA1", abc=True)

    try:
        while True:
            now = datetime.datetime.now()
            co2, temperature = co2_sensor1.readall()
            print("{}: co2 = {} [ppm], temp = {} [C]".format(now, co2, temperature))
            sleep(10.0)
    except KeyboardInterrupt:
        pass
