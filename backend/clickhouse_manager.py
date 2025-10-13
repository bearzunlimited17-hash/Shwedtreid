class ClickHouseManager:
    def __init__(self, host='localhost', port=9000, user='default', password=None, database='crypto_data'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def insert_candles(self, symbol, timeframe, rows):
        raise NotImplementedError('Insert to ClickHouse not implemented in this stub.')
