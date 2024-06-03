import pandas as pd
from datetime import datetime
from db_connection import MySQLConnection

class new_player:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self):
        query = f"SELECT timestamp, player_id FROM {table名稱}"
        records = self.db_connection.execute_query(query)
        return records

    def weekly_new_players(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'player_id'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.to_period('M')
        weekly_new_players = df.drop_duplicates(subset=['player_id']).groupby('timestamp').size().reset_index(name='new_players')
        weekly_new_players['timestamp'] = weekly_new_players['timestamp'].dt.to_timestamp()
        return weekly_new_players

    def insert_weekly_new_players(self,weekly_new_players):
        query = f"INSERT INTO {table名稱} (week, new_players) VALUES (%s, %s)"
        for index, row in weekly_new_players.iterrows():
            self.db_connection.execute_insert(query, (row['timestamp'], row['new_players']))