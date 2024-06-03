import pandas as pd
from datetime import datetime
from db_connection import MySQLConnection

class server_RAM_Std:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self):
        query = f"SELECT timestamp, value FROM {table名稱}"
        records = self.db_connection.execute_query(query)
        return records

    def daily_server_ram_std(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        daily_stats = df.resample('D', on='timestamp').agg(['mean', 'std']).reset_index()
        daily_stats.columns = ['timestamp', 'mean', 'std']
        return daily_stats

    def weekly_server_ram_std(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['week'] = df['timestamp'].dt.to_period('M')
        weekly_std = df.groupby('week')['value'].std().reset_index()
        weekly_std['week'] = weekly_std['week'].dt.to_timestamp()
        return weekly_std

    def insert_weekly_server_ram_std(self, weekly_std):
        query = f"INSERT INTO {table名稱} (week, std_dev) VALUES (%s, %s)"
        for index, row in weekly_std.iterrows():
            self.db_connection.execute_insert(query, (row['week'], row['value']))