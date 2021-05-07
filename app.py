import config
import asyncio
from bybit_api import Bybit_Api
import database
import comms
import logic
from strategy import vwap_cross_strat
import sql_connector as conn

test_tf = True # True for Testnet, False for Mainnet
run_strat = True # True to run strat code in main
setup_tables = False # True to setup all database tables
remove_tables = False # True to remove all database tables

symbol_pair = 'BTCUSD' # currently set for BTCUSD or ETHUSD
input_amount = 100
leverage = 5
input_quantity = input_amount * leverage 
entry_side = 'Buy'

if test_tf == True:
    api_key = config.BYBIT_TESTNET_API_KEY
    api_secret = config.BYBIT_TESTNET_API_SECRET
else:
    api_key = config.BYBIT_MAINNET_API_KEY
    api_secret = config.BYBIT_MAINNET_API_SECRET    

main_flag = True

def set_main_flag(true_false):
    main_flag = true_false

async def main():

    # setup & settings code:

    if (symbol_pair == "BTCUSD"):
        symbol = 'BTC'
        key_input = 0
        limit_price_difference = 0.50
    elif (symbol_pair == "ETHUSD"):
        symbol = 'ETH'
        key_input = 1
        limit_price_difference = 0.05
    else:
        print("Invalid Symbol Pair")

    api = Bybit_Api(api_key, api_secret, symbol, symbol_pair, key_input, test_tf)
    
    api.set_leverage(leverage)

    if setup_tables: conn.setup_tables()
    if remove_tables: conn.remove_all_tables()

    # strat code:
    active_trend = None
    
    while (run_strat):
        # run strat from strategy.vwap_cross_strat.py:
        print('checking strat values')
        position_size = api.get_position_size()

        trend = vwap_cross_strat.vwap_values_multiple_tf_trends()
        # Open new position when no position is open:
        if (position_size == 0):
            if (trend == 'uptrend'):
                # long:
                print(f'new trend: {trend} - opening long')
                api.place_order(price=api.last_price(),order_type='Market',side='Buy',input_quantity=input_quantity,stop_loss=0, reduce_only=False)
                active_trend = trend

                # short:
            elif (trend == 'downtrend'):
                print(f'new trend: {trend} - opening short')
                api.place_order(price=api.last_price(),order_type='Market',side='Sell',input_quantity=input_quantity,stop_loss=0, reduce_only=False)
                active_trend = trend

        # active position, check for close:
        elif (position_size > 0):
            # close on downtrend if in uptrend:
            if (active_trend == 'uptrend') and (trend == 'downtrend'):
                print(f'new trend: {trend} - closing long')
                api.place_order(price=api.last_price(),order_type='Market',side='Sell',input_quantity=position_size,stop_loss=0, reduce_only=True)
                active_trend = trend
            # close on uptrend if in downtrend:
            elif (active_trend == 'downtrend') and (trend == 'uptrend'):
                print(f'new trend: {trend} - closing short')
                api.place_order(price=api.last_price(),order_type='Market',side='Buy',input_quantity=position_size,stop_loss=0, reduce_only=True)
                active_trend = trend
            # prints while checking:
            else:
                print('active position:')
                print(f'position_sizee: {position_size}')
                print(f'pair last price: {api.last_price()}')
                print(f'active_trend: {active_trend}')

        await asyncio.sleep(5)

if __name__ == "__main__":  
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("closed by interrupt")
        loop.close()

