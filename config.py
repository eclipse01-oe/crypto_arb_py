"Basic configuration file for the arb finder"

DEFAULT_TAKER_FEE_PERCENT = 0.1
MIN_PROFIT_PERCENT = 0.2
MIN_TRADE_AMOUNT = 10
MAX_TRADE_AMOUNT = 1000
CHECK_INTERVAL_SECONDS = 5
TARGET_SYMBOLS = [
    'BTC/USDT',
    'ETH/USDT',
    'XRP/USDT',
    'SOL/USDT',
    'ADA/USDT'
]
EXCHANGE_IDS = ['binance', 'kucoin', 'gateio']
LOG_FILE = 'logs'
LOG_LEVEL = 'INFO'
