# -*- coding: utf-8 -*-
"""Thermometer ADT7410
https://akizukidenshi.com/catalog/g/gM-06675/

ADT7410 -- RasPi
================
VDD -- 3.3V (Pin1 or Pin17)
SCL -- I2C SCL (GPIO 3)
SDA -- I2C SDA (GPIO 2)
GND -- GND
"""
# from smbus import SMBus
from smbus2 import SMBus
import time


bus = SMBus(1)
address_adt7410 = 0x48
register_adt7410 = 0x00
data_bit = 13 # 13 or 16


### Reset ###
# bus.write_i2c_block_data(address_adt7410, 0x2F, [])
# time.sleep(0.001 * 0.2)


# ### Configuration (Table 11) ###
# if data_bit == 13:
#     bus.write_byte_data(address_adt7410, 0x03, 0x00)
# elif data_bit == 16:
#     bus.write_byte_data(address_adt7410, 0x03, 0x80)
# else:
#     raise ValueError(data_bit)


def sign13(x):
       return ( -(x & 0b1000000000000) |
                 (x & 0b0111111111111) )
def sign16(x):
       return ( -(x & 0b1000000000000000) |
                 (x & 0b0111111111111111) )


def adt7410_read():
    # word_data = bus.read_word_data(address_adt7410, register_adt7410)
    # data = (word_data & 0xff00)>>8 | (word_data & 0x00ff)<<8
    # if data_bit == 13:
    #     data = data>>3
    # elif data_bit == 16:
    #     pass
    # else:
    #     raise ValueError

    # if data & 0x1000 == 0:  # 温度が正または0の場合
    #     temperature = data*0.0625
    # else: # 温度が負の場合、 絶対値を取ってからマイナスをかける
    #     temperature = ( (~data&0x1fff) + 1)*-0.0625

    # ref: https://www.denshi.club/pc/raspi/5raspberry-pi-zeroiot194-i2c-adt7410.html
    if data_bit == 13:
        # bus.write_byte_data(address_adt7410, 0x03, 0x00)
        bus.write_byte_data(address_adt7410, 0x03, 0x20)
        time.sleep(240 * 0.001)
        data = bus.read_i2c_block_data(address_adt7410, register_adt7410, 2)
        raw = (((data[0]) << 8) | (data[1]) ) >> 3
        raw_s = sign13(int(hex(raw),16))
        temperature = raw_s * 0.0625
    elif data_bit == 16:
        # bus.write_byte_data(address_adt7410, 0x03, 0x80)
        bus.write_byte_data(address_adt7410, 0x03, 0xA0)
        time.sleep(240 * 0.001)
        data = bus.read_i2c_block_data(address_adt7410, register_adt7410, 2)
        raw = ((data[0]) << 8) | (data[1])
        raw_s = sign16(int(hex(raw),16))
        temperature = raw_s * 0.0078
    else:
        raise ValueError(data_bit)

    return temperature # [degree Celsius]



if __name__ == '__main__':
    from time import sleep
    import datetime

    try:
        while True:
            temperature = adt7410_read()
            now = datetime.datetime.now()
            print(now, temperature)
            sleep(10.0)
    except KeyboardInterrupt:
        pass

    bus.close()
