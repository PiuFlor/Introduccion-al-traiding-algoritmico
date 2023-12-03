from __future__ import (absolute_import, division, print_function, unicode_literals)
import math
import backtrader as bt


class TestStrategy(bt.Strategy):
    params = (
        ("bollinger_period", 20),
        ("bollinger_dev", 2),
        ("rsi_period", 5),
        ("rsi_overbought", 70),
        ("rsi_oversold", 30),
    )

    def __init__(self):
        self.dataClose = self.datas[0].close
        self.dataDate = None
        self.riesgo_por_operacion = 0.40
        self.riesgo_monetario = None
        self.tamaño_posición = None
        self.cantidad_comprar = 0
        self.porcentanje_perdida_permitido = 0.10
        self.precioCompra = 0

        # Bandas de Bollinger
        self.bollinger = bt.indicators.BollingerBands(self.dataClose, devfactor=self.params.bollinger_dev,
                                                      period=self.params.bollinger_period)
        # RSI
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # La orden ha sido enviada o aceptada
            return

        # Verifica si la orden fue completada
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('Compro, %.2f' % self.dataClose[0])
            elif order.issell():
                self.log('Vendio, %.2f' % self.dataClose[0])

    def next(self):

        if not self.position:
            # Estrategia de COMPRA
            if (self.dataClose[0] > self.bollinger.lines.bot[0] and self.rsi[0] < self.params.rsi_oversold or
                    (self.dataClose[0] > self.dataClose[-1]+self.dataClose[-1]*0.1) and (self.dataClose[0] > self.dataClose[-2]+self.dataClose[-2]*0.15)):
                self.riesgo_monetario = self.riesgo_por_operacion * self.broker.get_cash()
                self.tamaño_posición = math.floor(self.riesgo_monetario / (self.dataClose[0] - (self.dataClose[0] * self.porcentanje_perdida_permitido)))
                self.cantidad_comprar = min(self.data.volume[0], self.tamaño_posición)
                datetime_obj = self.datas[0].datetime.datetime()
                self.dataDate = datetime_obj
                self.buy(size=self.cantidad_comprar)
                self.precioCompra = self.dataClose[0]
            # Estrategia de Venta
        elif self.dataClose[0] < self.bollinger.lines.top[0] and self.rsi > self.params.rsi_overbought or self.precioCompra < self.dataClose[0]-self.dataClose[0]*0.4:
            self.sell(size=self.cantidad_comprar)

    def log(self, txt, dt=None, price=None):
        dt = dt or self.datas[0].datetime.date(0)
        price_info = f' (Precio: {price:.2f})' if price is not None else ''
        print('%s, %s%s' % (dt.isoformat(), txt, price_info))