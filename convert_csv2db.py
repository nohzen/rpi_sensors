import sqlite3
import pandas as pd


csv_path = 'datas/data_home.csv'
df = pd.read_csv(csv_path)
print(df.head())


db_path = 'datas/data_home.db'
connect = sqlite3.connect(db_path)
cursor = connect.cursor()
df.to_sql('sensor_data', connect, if_exists='replace', index=False)
# if_exists='fail', 'replace', 'append'

# Table list
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

# Table schema
cursor.execute("PRAGMA table_info(sensor_data)")
for row in cursor.fetchall():
    print(row)

# Data count
cursor.execute("SELECT COUNT(*) FROM sensor_data")
print(cursor.fetchone()[0])

# select_sql = 'SELECT * FROM sensor_data'
# for row in cursor.execute(select_sql):
#     print(row)


cursor.close()
connect.close()

