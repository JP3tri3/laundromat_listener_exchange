# example variables:

vwap_10_min = 0
vwap_15_min = 0
green_dot_30_min = False
rsi = 0

# sets the database variable value:
def set_vwap_10_min(param):
    vwap_10_min = param

# gets the database variable value:
def get_vwap_10_min():
    return vwap_10_min

# sets the database variable value:
def set_green_dot_30_min(param):
    green_dot_30_min = param

# gets the database variable value:
def get_green_dot_30_min():
    return green_dot_30_min

# repeat for any variables