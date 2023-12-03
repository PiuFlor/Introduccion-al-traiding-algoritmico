from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
from TestStrategy import TestStrategy
import backtrader as bt


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Configure the commission
    cerebro.broker.setcommission(commission=0.001)

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Ruta del archivo DOHLCV
    data = bt.feeds.GenericCSVData(dataname='C:/Users/Florencia/Desktop/Introducción al Trading Algorítmico/orcl-1995-2014.txt',
                                   fromdate=datetime.datetime(1995, 1, 1),
                                   todate=datetime.datetime(2014, 12, 31),
                                   dtformat=('%Y-%m-%d'),
                                   open=1, high=2, low=3, close=4, adj_close=5, volume=6)
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())