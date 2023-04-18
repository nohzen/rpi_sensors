# Prepair environment
```sh
# Raspberry Pi setting
## I2C
sudo raspi-config nonint do_i2c 0
sudo apt install i2c-tools
## SPI
sudo raspi-config nonint do_spi 0
## Serial
sudo raspi-config nonint do_serial 2

# Add permission to use mh_z19 without root
# ref: https://github.com/UedaTakeyuki/mh-z19/wiki/How-to-use-without-root-permission.
ls -la /dev/ttyS0
crw--w---- 1 root tty 4, 64 Mar  4 00:57 /dev/ttyS0
sudo chmod g+r /dev/ttyS0
ls -la /dev/ttyS0
crw-rw---- 1 root tty 4, 64 Mar  4 00:57 /dev/ttyS0

# Clone codes
git clone git@github.com:nohzen/rpi_sensors.git

# Python libraries
sudo apt install python3-pip
python -m pip install --upgrade pip setuptools
pip install smbus2
pip install mh_z19
pip install streamlit
pip install matplotlib
pip install pandas
pip install Jinja2 --upgrade
```

## 32bit OS
pyarrow which streamlit use don't work on 32bit OS.
https://discuss.streamlit.io/t/raspberry-pi-streamlit/2900?page=2
```sh
pip install pyarrow

      Traceback (most recent call last):
        File "/home/nohzen/.local/bin/cmake", line 5, in <module>
          from cmake import cmake
      ModuleNotFoundError: No module named 'cmake'
      error: command '/home/nohzen/.local/bin/cmake' failed with exit code 1
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for pyarrow
Failed to build pyarrow
ERROR: Could not build wheels for pyarrow, which is required to install pyproject.toml-based projects
```


# How to use python scripts
```sh
# Get sensor values
python main_sensor.py --csv_path path/to/csv --place home

# Start streamlit dashboard
python -m streamlit run dashboard_streamlit.py --server.headless true -- --csv_path path/to/csv --place home
```


# Daemon
- Sensor capture daemon
`/etc/systemd/system/my_sensor.service`
```
[Unit]
Description=Start rpi sensors
After=network.target

[Service]
User=nohzen
WorkingDirectory=/path/to/code_dir
ExecStart=/usr/bin/python3 main_sensor.py --csv_path path/to/csv --place home

[Install]
WantedBy=multi-user.target
```

- Streamlit dashboard daemon
`/etc/systemd/system/dashboard_streamlit.service`
```
[Unit]
Description=Server of streamlit dashboard
After=network.target

[Service]
User=nohzen
WorkingDirectory=/path/to/code_dir
ExecStart=/usr/bin/python3 -m streamlit run dashboard_streamlit.py --server.headless true -- --csv_path path/to/csv --place home

[Install]
WantedBy=multi-user.target
```

- systemd
```sh
# Reload servies
sudo systemctl daemon-reload

# start/stop services
sudo systemctl enable my_sensor
sudo systemctl disable my_sensor
sudo systemctl start my_sensor
sudo systemctl stop my_sensor
systemctl status my_sensor
```

