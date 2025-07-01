"for exchange interactions"

import os
import ccxt
from dotenv import load_dotenv
from utils import Logger

class ExchangeManager:
    """
    Manages connections and interactions with multiple cryptocurrency exchanges.
    """
    def __init__(self, exchange_ids):
        """
        Initializes exchange instances for the given IDs.
        Loads API keys from environment variables.
        """
        self.exchanges = {}
        load_dotenv() # Load .env file

        for ex_id in exchange_ids:
            try:
                # Get API key and secret from environment variables
                api_key = os.getenv(f"{ex_id.upper()}_API_KEY")
                secret = os.getenv(f"{ex_id.upper()}_SECRET")

                if not api_key or not secret:
                    Logger.warning("API key or secret not found for %s. Skipping this exchange.", ex_id.upper())
                    continue

                exchange_class = getattr(ccxt, ex_id)
                exchange = exchange_class({
                    'apiKey': api_key,
                    'secret': secret,
                    'enableRateLimit': True, # Enable ccxt's built-in rate limiter
                })
                self.exchanges[ex_id] = exchange
                Logger.info("Successfully initialized %s exchange.", ex_id)
            except (AttributeError, TypeError, ccxt.BaseError) as e:
                Logger.error("Error initializing %s exchange: %s", ex_id, e)

    async def fetch_ticker(self, exchange_id, symbol):
        """
        Fetches the ticker for a given symbol from a specific exchange.
        Returns a dictionary with 'bid', 'ask', 'timestamp', 'exchange_id', 'symbol'.
        """
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            Logger.warning("Exchange %s not initialized.", exchange_id)
            return None
        
        try:
            ticker = await exchange.fetch_ticker(symbol)
            return {
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'timestamp': ticker['timestamp'],
                'exchange_id': exchange_id,
                'symbol': symbol
            }
        except ccxt.NetworkError as e:
            Logger.error("Network error fetching %s from %s: %s", symbol, exchange_id, e)
            return None
        except ccxt.ExchangeError as e:
            Logger.error("Exchange error fetching %s from %s: %s", symbol, exchange_id, e)
            return None
        except Exception as e:
            Logger.error("Unexpected error fetching %s from %s: %s", symbol, exchange_id, e)
            return None

    async def fetch_balance(self, exchange_id, currency):
        """
        Fetches the available balance for a specific currency on an exchange.
        """
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            Logger.warning("Exchange %s not initialized.", exchange_id)
            return 0.0
        try:
            balance = await exchange.fetch_balance()
            return balance['free'].get(currency, 0.0)
        except Exception as e:
            Logger.error("Error fetching balance for %s on %s: %s", currency, exchange_id, e)
            return 0.0

    async def create_market_buy_order(self, exchange_id, symbol, amount):
        """
        Simulates placing a market buy order.
        In a real bot, this would interact with the exchange API.
        """
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            Logger.warning("Exchange %s not initialized.", exchange_id)
            return None
        try:
            # THIS IS A SIMULATED ORDER. Replace with actual API call for live trading.
            # order = await exchange.create_market_buy_order(symbol, amount)
            Logger.info("SIMULATED BUY ORDER: %s - %s - Amount: %s", exchange_id, symbol, amount)
            # Simulate a successful order response
            return {'id': f'sim_buy_order_{exchange_id}_{symbol}_{amount}', 'status': 'closed', 'amount': amount}
        except Exception as e:
            Logger.error("Error simulating buy order on %s for %s amount %s: %s", exchange_id, symbol, amount, e)
            return None

    async def create_market_sell_order(self, exchange_id, symbol, amount):
        """
        Simulates placing a market sell order.
        In a real bot, this would interact with the exchange API.
        """
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            Logger.warning("Exchange %s not initialized.", exchange_id)
            return None
        try:
            # THIS IS A SIMULATED ORDER. Replace with actual API call for live trading.
            # order = await exchange.create_market_sell_order(symbol, amount)
            Logger.info("SIMULATED SELL ORDER: %s - %s - Amount: %s", exchange_id, symbol, amount)
            # Simulate a successful order response
            return {'id': f'sim_sell_order_{exchange_id}_{symbol}_{amount}', 'status': 'closed', 'amount': amount}
        except ccxt.BaseError as e:
            Logger.error("Error simulating sell order on %s for %s amount %s: %s", exchange_id, symbol, amount, e)
            return None
