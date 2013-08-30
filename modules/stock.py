# Description:
#   Stock lookup module
#
# Commands:
#
#   !stock <ticker> - show todays stock chart for <ticket>
#
# Dependencies:
#  ystockquote

from botulus.basemodule import BaseModule
import ystockquote


class Stock(BaseModule):
    """ Stock lookup module """
    def default(self, args=None):
        stock_data = (args[0], ystockquote.get_price(args[0]))
        return "Current stock price of %s: %s" % stock_data

__module__ = Stock
