import sys
sys.path.append("..")
import sql_connector as conn
from bybit_api import Bybit_Api
import asyncio

class VWAP_Cross_Strat:

    def __init__(self, limit_price_difference, input_quantity, api_key, api_secret, symbol, symbol_pair, key_input, test_tf):
        self.limit_price_difference = limit_price_difference
        self.input_quantity = input_quantity
        
        self.api = Bybit_Api(api_key, api_secret, symbol, symbol_pair, key_input, test_tf)


        print('... VWAP_Cross_Strat initialized...')

    async def main_vwap_cross_strat(self):
        
        # set strat variables:
        # entry should work with Limit or Market:
        entry_market_type = 'Limit'
        # exit can work with both, but if using Limit the price has to be set so the order isn't cancelled when placed:
        exit_market_type = 'Market'

        # set to True to use a chasing limit entry order:
        chasing_limit_entry = True
        # set the limit order wait time before chasing:
        reset_order_time = 10

        # set the interval strat wide interval for waiting during 'sleep' states 
        interval = 2

        # set stop loss value in contracts currently, example: 200:
        stop_loss = 200

        # initialize strat:
        print('initializing main_vwap_cross_strat')
        active_trend = None
        trend = None

        while (True):

            # Search for trend in loop while trend = None
            while (trend == None):
                print('\nchecking strat values')
                trend = self.vwap_values_multiple_tf_trends()
                print(f'trend: {trend}')
                await asyncio.sleep(interval)

            # breaks out of loop when trend != none ('!=' means 'does not equal')
            
            # updates input quantity to match remainder for partially filled orders
            position_size = self.api.get_position_size()
            initial_input_quantity = self.input_quantity
            input_quantity = initial_input_quantity - position_size

            # makes sure no open position before addressing new position:
            if (position_size == initial_input_quantity):
                print('there is currently an active full position')
            
            # Open new position when no position is open:
            else:
                if (trend == 'uptrend') or (trend == 'downtrend'):
                    # trend was confirmed, determining side:
                    if (trend == 'uptrend'):
                        # long:
                        print(f'new trend: {trend} - opening long')
                        price = self.api.last_price() - self.limit_price_difference
                        side = 'Buy'
                        calculated_stop_loss = price - stop_loss

                    elif (trend == 'downtrend'):
                        # short parameters
                        print(f'new trend: {trend} - opening short')
                        price = self.api.last_price() + self.limit_price_difference
                        side = 'Sell'
                        calculated_stop_loss = price + stop_loss
                    
                    # checks number of orders, determines whether or not to create a new order or change a previous entry order:
                    num_open_orders = len(self.api.get_orders())
                    if (num_open_orders == 0):
                        self.api.place_order(price=price,order_type=entry_market_type,side=side,input_quantity=input_quantity,stop_loss=calculated_stop_loss, reduce_only=False)
                    else:
                        order_id = self.api.get_order_id()
                        self.api.change_order_price_size(price, input_quantity, order_id)
                    
                    # sets active trend:
                    active_trend = trend
                    trend = None

                else:
                    # skips the order if trend wasn't confirmed
                    print('invalid trend, going back to determine trend')
                    print(f'trend: {trend}')


            # stop in loop and check the amount of active unfilled orders
            order_timer = 0
            order_check = True

            while (order_check):
                num_open_orders = len(self.api.get_orders())
                if (num_open_orders == 0):
                    print(f'{num_open_orders} unfilled orders')
                    order_check = False

                else:
                    print('\nwaiting for order to be filled')
                    await asyncio.sleep(interval)
                    # use chasing_limit_entry:
                    if (chasing_limit_entry):
                        print('chasing_limit_entry: ')
                        order_timer += interval
                        print(f'unfilled order timer: {order_timer}')
                        if (order_timer >= reset_order_time):
                            order_check = False
                    
            # breaks out of loop when order is filled and active unfilled orders == 0, or if unfilled order after 30 seconds

            # checks for partial fills before waiting on close position:
            if (self.api.get_position_size() == initial_input_quantity):
                active_position_flag = True
            else:
                active_position_flag = False

            # active position with full input quantity, stay in loop checking for close while active_position_flag = True:
            while (active_position_flag):
                position_size = self.api.get_position_size()
                print(f'position_size: {position_size}')
                trend = self.vwap_values_multiple_tf_trends()

                # close on downtrend if in uptrend:
                if (active_trend == 'uptrend') and (trend == 'downtrend'):
                    # close long:
                    print(f'new trend: {trend} - closing long')
                    price = self.api.last_price()
                    # take_profit is the exit price, can change if using limit exits
                    take_profit = price
                    self.api.place_order(price=take_profit,order_type=exit_market_type,side='Sell',input_quantity=position_size,stop_loss=0, reduce_only=True)
                    active_trend = trend
                # close on uptrend if in downtrend:
                elif (active_trend == 'downtrend') and (trend == 'uptrend'):
                    # close short
                    print(f'new trend: {trend} - closing short')
                    price = self.api.last_price()
                    # take_profit is the exit price, can change if using limit exits
                    take_profit = price
                    self.api.place_order(price=take_profit,order_type=exit_market_type,side='Buy',input_quantity=position_size,stop_loss=0, reduce_only=True)
                    active_trend = trend
                # prints while checking:
                else:
                    print('active position:')
                    print(f'position_sizee: {position_size}')
                    print(f'pair last price: {self.api.last_price()}')
                    print(f'active_trend: {active_trend}')

                # if position_size == 0, change active_position_flag = False, break out of loop
                if (position_size == 0):
                    active_position_flag = False

                # sleep in loop, checks for changes set to every 5 seconds. 
                await asyncio.sleep(interval)

        # start main loop over




    # determine vwap trend from 'up' / 'down' 
    def vwap_values_multiple_tf_trends(self):
        vwap_trend = None

        # retrieve values from table via sql_connector.py:
        vwap_15m_trend = conn.get_last_row_value('15m', 'vwap_mcb_trend')
        vwap_1hr_trend = conn.get_last_row_value('1hr', 'vwap_mcb_trend')
        vwap_4hr_trend = conn.get_last_row_value('4hr', 'vwap_mcb_trend')
        vwap_1d_trend = conn.get_last_row_value('1d', 'vwap_mcb_trend')

        # TEST PRINTS: 
        print(f'vwap_15m: {vwap_15m_trend}, vwap_1hr: {vwap_1hr_trend}, vwap_4hr: {vwap_4hr_trend}, vwap_1d: {vwap_1d_trend}')

        # compare values:
        if (vwap_15m_trend == 'up') and (vwap_1hr_trend == 'up') \
            and (vwap_4hr_trend == 'up') and (vwap_1d_trend == 'up'):
            return 'uptrend'
        elif (vwap_15m_trend == 'down') and (vwap_1hr_trend == 'down') \
            and (vwap_4hr_trend == 'down') and (vwap_1d_trend == 'down'):
            return 'downtrend'
        else:
            return None


    # determine vwap trend from numerical values
    def vwap_values_multiple_tf(self):
        vwap_trend = None

        # retrieve values from table via sql_connector.py:
        vwap_15m = conn.get_last_row_value('15m', 'vwap_mcb')
        vwap_1hr = conn.get_last_row_value('1hr', 'vwap_mcb')
        vwap_4hr = conn.get_last_row_value('4hr', 'vwap_mcb')
        vwap_1d = conn.get_last_row_value('1d', 'vwap_mcb')

        # sets condition check:
        vwap_15m_check = None
        vwap_1hr_check = None
        vwap_4hr_check = None
        vwap_1d_check = None

        # check conditions:
        min_positive = 0

        if vwap_15m_check >= min_positive:
            vwap_15m_check = True

        if vwap_1hr_check >= min_positive:
            vwap_1hr_check = True

        if vwap_4hr_check >= min_positive:
            vwap_4hr_check = True

        if vwap_1d_check >= min_positive:
            vwap_1d_check = True

        # determine if all vwap checks = True:
        if vwap_15m_check and vwap_1hr_check and vwap_4hr_check and vwap_1d_check:
            vwap_trend = 'uptrend'
        elif (vwap_15m_check == False) and (vwap_1hr_check == False) and \
            (vwap_4hr_check == False) and (vwap_1d_check == False):
            vwap_trend = 'downtrend'
        else:
            vwap_trend = 'notrend'

        return vwap_trend


