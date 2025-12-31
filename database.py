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

        # Data count
        self.cursor.execute("SELECT COUNT(*) FROM sensor_data")
        print("Data count:", self.cursor.fetchone()[0])
        self.cursor.execute("SELECT COUNT(switchbot_hub3_humidity) FROM sensor_data")
        print("Data count:", self.cursor.fetchone())

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

    # db.add_column('switchbot_meter_temperature', 'REAL')
    # db.add_column('switchbot_meter_humidity', 'REAL')
    # db.add_column('switchbot_outdoor_meter_temperature', 'REAL')
    # db.add_column('switchbot_outdoor_meter_humidity', 'REAL')
    # db.add_column('switchbot_hub3_temperature', 'REAL')
    # db.add_column('switchbot_hub3_humidity', 'REAL')

    # db.convert_csv_to_db(csv_path)
    db.show_db_info()


    data_dict = {
        'datetime': '2024-06-01 12:00:00',
        'switchbot_meter_temperature': 23.5,
        'switchbot_meter_humidity': 45.2,
        'switchbot_hub3_temperature': 18.3,
        'switchbot_hub3_humidity': 55.1
    }
    db.add_data(data_dict)

    db.show_db_info()

