import sqlite3
import pandas as pd
import sys


# Check Python version for dict orderedness (Python 3.7+)
REQUIRED = (3, 7)
if sys.version_info < REQUIRED:
    raise RuntimeError(
        f"Python {REQUIRED[0]}.{REQUIRED[1]} is required. "
        f"(current: {sys.version_info.major}.{sys.version_info.minor})"
    )


def plot_monthly_data_count(df):
    import matplotlib.pyplot as plt

    df['Date'] = pd.to_datetime(df['Date'])
    monthly_counts = df.resample('ME', on='Date').size()
    counts_per_hour = monthly_counts / 30.0 / 24.0

    fig, ax = plt.subplots()
    ax.plot(
        counts_per_hour.index,
        counts_per_hour.values,
        marker='o',
        linestyle='-'
    )

    ax.set_xlabel('Month')
    ax.set_ylabel('Number of data points per hour')
    ax.set_title('Monthly data count')
    ax.grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


class SensorDataDB:
    def __init__(self, db_path='datas/data_home.db'):
        self.db_path = db_path

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def convert_csv_to_db(self, csv_path='datas/data_home.csv'):
        df = pd.read_csv(csv_path)
        print(df.head())
        df.to_sql('sensor_data', self.conn, if_exists='replace', index=False)
        # if_exists='fail', 'replace', 'append'

    def convert_switchbot_csv_to_db(self, csv_path='datas/switchbot_data.csv'):
        df = pd.read_csv(csv_path)
        print(df.head())

        # plot_monthly_data_count(df)

        temperature_name = "switchbot_hub3_temperature"
        humidity_name = "switchbot_hub3_humidity"
        df = df.drop(columns=[
            "DPT(℃)",
            "VPD(kPa)",
            "Abs Humidity(g/m³)",
            "Light_Value"
        ], errors="raise")
        df = df.rename(columns={
            "Date": "datetime",
            "Temperature_Celsius(℃)": temperature_name,
            "Relative_Humidity(%)": humidity_name,
        })
        df["datetime"] = pd.to_datetime(df["datetime"], errors="raise")
        # print(df.head())

        df.to_sql('sensor_data', self.conn, if_exists='append', index=False)

    def show_db_info(self):
        # Table list
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print("Tables:", self.cursor.fetchall())

        # Table schema
        self.cursor.execute("PRAGMA table_info(sensor_data)")
        print("Table schema:")
        # cid, name, type, notnull(nullを許すか), dflt_value(default value), pk(primary key)
        for row in self.cursor.fetchall():
            print(row)
            name = row[1]
            self.cursor.execute(f"SELECT COUNT({name}) FROM sensor_data")
            print(f"    count: ", self.cursor.fetchone()[0])

        # Data count
        self.cursor.execute("SELECT COUNT(*) FROM sensor_data")
        print("Total count:", self.cursor.fetchone()[0])

        # Show some data
        self.cursor.execute("""
            SELECT *
            FROM sensor_data
            ORDER BY RANDOM()
            LIMIT 5
        """)
        for row in self.cursor.fetchall():
            print(row)

        # select_sql = 'SELECT * FROM sensor_data'
        # for row in self.cursor.execute(select_sql):
        #     print(row)

    def add_column(self, column_name, column_type='REAL'):
        alter_sql = f'ALTER TABLE sensor_data ADD COLUMN {column_name} {column_type}'
        self.cursor.execute(alter_sql)
        self.conn.commit()

    def add_data(self, data_dict):
        if "datetime" not in data_dict:
            raise ValueError("data_dict must include datetime key")
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['?'] * len(data_dict))
        insert_sql = f'INSERT INTO sensor_data ({columns}) VALUES ({placeholders})'
        self.cursor.execute(insert_sql, tuple(data_dict.values()))
        self.conn.commit()



if __name__ == '__main__':
    csv_path = './datas/data_home.csv'
    db_path = './datas/data_home.db'

    db = SensorDataDB(db_path)
    db.show_db_info()

    ### Add switchbot datas from csv ###
    # db.convert_switchbot_csv_to_db(csv_path="datas/hub3_data.csv")
    # db.show_db_info()

    ### Add columns for SwitchBot sensors
    # db.add_column('switchbot_meter_temperature', 'REAL')
    # db.add_column('switchbot_meter_humidity', 'REAL')
    # db.add_column('switchbot_outdoor_meter_temperature', 'REAL')
    # db.add_column('switchbot_outdoor_meter_humidity', 'REAL')
    # db.add_column('switchbot_hub3_temperature', 'REAL')
    # db.add_column('switchbot_hub3_humidity', 'REAL')
    # db.show_db_info()


