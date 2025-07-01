"Finds arbitrage opportunity"

from config import MIN_PROFIT_PERCENT, DEFAULT_TAKER_FEE_PERCENT

class ArbitrageFinder:
    """
    Identifies cross-exchange arbitrage opportunities.
    """
    def __init__(self):
        pass

    def find_best_opportunity(self, all_market_data):
        """
        Finds the best cross-exchange arbitrage opportunity across all
        monitored symbols and exchanges.

        Args:
            all_market_data (dict): A dictionary of market data
                                   {(symbol, exchange_id): {bid, ask, timestamp}}.

        Returns:
            dict or None: A dictionary describing the best opportunity found,
                          or None if no profitable opportunity exists.
        """
        best_opportunity = None
        highest_net_profit_percent = MIN_PROFIT_PERCENT # Only consider opportunities above this threshold

        # Get all unique symbols present in the market data
        all_symbols = set(key[0] for key in all_market_data.keys())

        for symbol in all_symbols:
            # Find all exchanges that have data for this symbol
            exchanges_with_symbol = [
                ex_id for (sym, ex_id) in all_market_data.keys() if sym == symbol
            ]

            if len(exchanges_with_symbol) < 2:
                continue # Need at least two exchanges for cross-exchange arbitrage

            # Iterate through all possible buy-sell exchange pairs for this symbol
            for buy_exchange_id in exchanges_with_symbol:
                for sell_exchange_id in exchanges_with_symbol:
                    if buy_exchange_id == sell_exchange_id:
                        continue # Cannot arbitrage on the same exchange for cross-exchange

                    buy_data = all_market_data.get((symbol, buy_exchange_id))
                    sell_data = all_market_data.get((symbol, sell_exchange_id))

                    # Ensure we have valid bid/ask prices for both
                    if not buy_data or not sell_data or \
                       buy_data['ask'] is None or sell_data['bid'] is None:
                        continue

                    buy_price = buy_data['ask'] # Price to buy at (lowest ask)
                    sell_price = sell_data['bid'] # Price to sell at (highest bid)

                    # Basic check for potential profit before fee calculation
                    if sell_price <= buy_price:
                        continue

                    # --- Fee Calculation (Simplified) ---
                    # In a real bot, you'd fetch actual taker fees for each exchange/symbol
                    # and potentially consider maker fees if placing limit orders.
                    # Also, withdrawal fees for rebalancing are a major factor.
                    buy_fee_percent = DEFAULT_TAKER_FEE_PERCENT
                    sell_fee_percent = DEFAULT_TAKER_FEE_PERCENT

                    # Calculate effective prices after fees
                    # Buying: initial_capital / (1 + fee_percent/100)
                    # Selling: received_amount * (1 - fee_percent/100)
                    
                    # Cost to acquire 1 unit of crypto on buy_exchange
                    cost_per_unit = buy_price * (1 + buy_fee_percent / 100)
                    
                    # Revenue from selling 1 unit of crypto on sell_exchange
                    revenue_per_unit = sell_price * (1 - sell_fee_percent / 100)

                    if revenue_per_unit > cost_per_unit:
                        net_profit_percent = ((revenue_per_unit - cost_per_unit) / cost_per_unit) * 100

                        if net_profit_percent > highest_net_profit_percent:
                            highest_net_profit_percent = net_profit_percent
                            best_opportunity = {
                                'symbol': symbol,
                                'buy_exchange': buy_exchange_id,
                                'sell_exchange': sell_exchange_id,
                                'buy_price': buy_price,
                                'sell_price': sell_price,
                                'net_profit_percent': net_profit_percent,
                                'estimated_buy_fee_percent': buy_fee_percent,
                                'estimated_sell_fee_percent': sell_fee_percent
                            }
        return best_opportunity
