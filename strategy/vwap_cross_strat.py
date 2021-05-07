import sql_connector as conn



def vwap_values_multiple_tf():
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
        (vwap_15vwap_4hr_checkm_check == False) and (vwap_1d_check == False):
        vwap_trend = 'downtrend'
    else:
        vwap_trend = 'notrend'

    return vwap_trend


def vwap_values_multiple_tf_trends():
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