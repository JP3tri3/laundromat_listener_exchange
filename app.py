import config
import asyncio
from bybit_api import Bybit_Api
import database
import comms
import logic
from strategy import vwap_cross_strat

test_tf = True # True for Testnet, False for Mainnet
leverage = 5
symbol_pair = 'BTCUSD' # currently set for BTCUSD or ETHUSD
input_quantity = 100 * leverage 
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

    # run strat from strategy.vwap_cross:
    print('checking strat values')
    if (vwap_cross_strat.vwap_values_multiple_tf() == 'uptrend'):
        # long:
        api.place_order(price=api.last_price(),order_type='Market',side='Buy',input_quantity=input_quantity,stop_loss=0, reduce_only=False)
        # short:
    elif (vwap_cross_strat.vwap_values_multiple_tf() == 'downtrend'):
        api.place_order(price=api.last_price(),order_type='Market',side='Sell',input_quantity=input_quantity,stop_loss=0, reduce_only=False)
    else:
        print('waiting on trigger')

    await asyncio.sleep(30)

if __name__ == "__main__":  
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("closed by interrupt")
        loop.close()

