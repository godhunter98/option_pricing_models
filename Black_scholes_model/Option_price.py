from model import *


# Initialize with example data
model = OptionPricingModel(spot=140, strike_price=100, rfr=0.1, volatility=0.3,time_to_expiry=.5)

# Call the functions
print("d1:", model.d1())
print("N(d1):", model.normsd1())
print("d2:", model.d2())
print("N(d2):", model.normsd2())
print("Call option Price is:", round(model.call_option_price(),3))
print('Put option Price is: ',round(model.put_option_price(),3))
