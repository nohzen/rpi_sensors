# Python scripts
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

