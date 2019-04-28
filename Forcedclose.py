# from GlobalPramaters import *
# from Global import *

from globalparameters import *
from global0 import *


for symbol in SYMBOLS:
    order.insert_closePosition(symbol)
order.execute()

