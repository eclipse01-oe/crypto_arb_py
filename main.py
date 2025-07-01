"main script"

import asyncio
import time
from config import EXCHANGE_IDS, CHECK_INTERVAL_SECONDS, TARGET_SYMBOLS
from utils import Logger
from exc_mngr import ExchangeManager
from data_mngr import DataManager
from arb_fndr import ArbitrageFinder
from trade_exec import TradeExecutor

async def main():
    """
    Main function to run the crypto arbitrage bot.
    """
    Logger.info("Starting Crypto Arbitrage Bot...")

    # 1. Initialize Exchange Manager
    exchange_manager = ExchangeManager(EXCHANGE_IDS)
    if not exchange_manager.exchanges:
        Logger.critical("No exchanges initialized. Exiting.")
        return

    # 2. Initialize Data Manager and start fetching tickers in background
    data_manager = DataManager(exchange_manager)
    # Start the periodic ticker fetching as a background task
    asyncio.create_task(data_manager.fetch_all_tickers_periodically())
    Logger.info("Started background data fetching for %s on %s.", TARGET_SYMBOLS, EXCHANGE_IDS)

    # Give some time for initial data to be fetched
    Logger.info("Waiting %d seconds for initial market data...", CHECK_INTERVAL_SECONDS * 2)
    await asyncio.sleep(CHECK_INTERVAL_SECONDS * 2) 

    # 3. Initialize Arbitrage Finder and Trade Executor
    arbitrage_finder = ArbitrageFinder()
    trade_executor = TradeExecutor(exchange_manager)

    Logger.info("Bot is now actively looking for opportunities...")

    while True:
        try:
            # Get the latest market data
            current_market_data = data_manager.get_latest_market_data()

            if not current_market_data:
                Logger.warning("No market data available yet. Waiting...")
                await asyncio.sleep(CHECK_INTERVAL_SECONDS)
                continue

            # 4. Find the best arbitrage opportunity
            best_opportunity = arbitrage_finder.find_best_opportunity(current_market_data)

            if best_opportunity:
                Logger.info("Potential Arbitrage Found: %s - Buy on %s @ %s | Sell on %s @ %s | Net Profit: %.4f%%",
                            best_opportunity['symbol'], best_opportunity['buy_exchange'], best_opportunity['buy_price'],
                            best_opportunity['sell_exchange'], best_opportunity['sell_price'], best_opportunity['net_profit_percent'])
                
                # 5. Execute the trade (SIMULATED)
                await trade_executor.execute_arbitrage_trade(best_opportunity)
            else:
                Logger.info("No profitable arbitrage opportunities found at the moment.")

        except Exception as e:
            Logger.error("An unexpected error occurred in the main loop: %s",e)

        # Wait before the next check
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    # Run the asyncio event loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Logger.info("Bot stopped by user (KeyboardInterrupt).")
    except Exception as e:
        Logger.critical("Bot crashed: %s", e)