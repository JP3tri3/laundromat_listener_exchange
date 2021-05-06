import sql_connector as conn



def vwap_values_multiple_tf():
    vwap_trend = None

    # retrieve values from table:
    vwap_15m = conn.get_last_row_value('15m', 'vwap_mcb')
    vwap_1hr = conn.get_last_row_value('1hr', 'vwap_mcb')
    vwap_4hr = conn.get_last_row_value('4hr', 'vwap_mcb')
    vwap_1d = conn.get_last_row_value('1d', 'vwap_mcb')

    # sets condition check:
    vwap_15m_check = False
    vwap_1hr_check = False
    vwap_4hr_check = False
    vwap_1d_check = False

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
