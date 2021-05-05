import config
import asyncio
from bybit_api import Bybit_Api
import database
import comms
import logic

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

    #     if (green_dot_30_min == True) and (vwap_10_min > 10):

    #         # # use any of the order functions in bybit_api.py
    #         api.place_order(price, order_type, side, input_quantity, stop_loss, reduce_only)

    #         # # confirm position:
    #         if (api.get_position_size() > 0):
    #             # # Set up monitoring for close etc etc etc
    #             print(f'current price: {api.last_price()}')
    #         else:
    #             # # try to place order again or check variables again
    #             api.place_order(price, order_type, side, input_quantity, stop_loss, reduce_only)

    #     else:
    #         # # Set main_flag back to false if initial conditions weren't met, 
    #         # # waiting for next webhook alert
    #         main_flag = False





if __name__ == "__main__":  
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("closed by interrupt")
        loop.close()

