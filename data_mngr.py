"manages price data"

import asyncio
from utils import Logger
from config import EXCHANGE_IDS, TARGET_SYMBOLS, CHECK_INTERVAL_SECONDS

class DataManager:
    """
    Manages fetching and storing real-time market data from multiple exchanges.
    """
    def __init__(self, exchange_manager):
        self.exchange_manager = exchange_manager
        # Stores the latest ticker data: {(symbol, exchange_id): {bid, ask, timestamp}}
        self.market_data = {}
        self.last_fetch_time = {} # To track last update for each (symbol, exchange)

    async def fetch_all_tickers_periodically(self):
        """
        Continuously fetches tickers for all target symbols across all configured exchanges.
        This runs as a background task.
        """
        while True:
            tasks = []
            for ex_id in EXCHANGE_IDS:
                for symbol in TARGET_SYMBOLS:
                    tasks.append(self._fetch_and_update_ticker(ex_id, symbol))
            
            await asyncio.gather(*tasks)
            await asyncio.sleep(CHECK_INTERVAL_SECONDS) # Wait before next fetch cycle

    async def _fetch_and_update_ticker(self, ex_id, symbol):
        """
        Fetches a single ticker and updates the in-memory market_data.
        """
        ticker_data = await self.exchange_manager.fetch_ticker(ex_id, symbol)
        if ticker_data:
            key = (symbol, ex_id)
            self.market_data[key] = ticker_data
            self.last_fetch_time[key] = asyncio.get_event_loop().time() # Record fetch time
            # logger.debug(f"Updated {symbol} on {ex_id}: Bid={ticker_data['bid']}, Ask={ticker_data['ask']}")
        else:
            Logger.warning("Failed to fetch ticker for %s on %s.", symbol, ex_id)

    def get_latest_market_data(self):
        """
        Returns a copy of the current in-memory market data.
        """
        return self.market_data.copy()

    def is_data_stale(self, symbol, exchange_id, max_staleness_seconds=10):
        """
        Checks if the data for a specific symbol on an exchange is stale.
        """
        key = (symbol, exchange_id)
        if key not in self.last_fetch_time:
            return True # No data ever fetched
        
        current_time = asyncio.get_event_loop().time()
        if (current_time - self.last_fetch_time[key]) > max_staleness_seconds:
            Logger.warning(
                "Data for %s on %s is stale (last updated %.2fs ago).",
                symbol, exchange_id, current_time - self.last_fetch_time[key]
            )
            return True
        return False
