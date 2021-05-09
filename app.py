import config
import asyncio
from bybit_api import Bybit_Api
import database
import comms
import logic
from strategy.vwap_cross_strat import VWAP_Cross_Strat
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
    vwap_cross_strat = VWAP_Cross_Strat(limit_price_difference, input_quantity, api_key, api_secret, symbol, symbol_pair, key_input, test_tf)

    api.set_leverage(leverage)

    if setup_tables: conn.setup_tables()
    if remove_tables: conn.remove_all_tables()
    
    while (run_strat):


        await vwap_cross_strat.main_vwap_cross_strat()



if __name__ == "__main__":  
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        loop.close()
        print("closed by interrupt")
        

