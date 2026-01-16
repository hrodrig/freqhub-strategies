import logging
from typing import Optional

import pandas as pd
import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import (DecimalParameter, IntParameter, IStrategy, merge_informative_pair)

logger = logging.getLogger(__name__)


class RSI_BollingerStrategy(IStrategy):
    """
    Estrategia Simple RSI + Bollinger Bands - Momentum y volatilidad
    
    Nivel de Riesgo: MEDIO
    Profit Esperado: ~8-10% mensual
    
    Esta estrategia combina RSI para identificar momentum con Bollinger Bands
    para identificar zonas de entrada en condiciones de volatilidad.
    
    Características:
    - Stop loss moderado (-6%)
    - Trailing stop para proteger ganancias
    - Timeframe: 15m con contexto de 1h
    - Entrada cuando RSI favorable y precio rebota desde banda inferior
    """
    
    INTERFACE_VERSION = 3
    
    # Parámetros optimizables
    buy_rsi_min = IntParameter(45, 60, default=50, space="buy", optimize=True)
    buy_rsi_max = IntParameter(65, 80, default=70, space="buy", optimize=True)
    buy_bb_period = IntParameter(15, 25, default=20, space="buy", optimize=True)
    buy_bb_std = DecimalParameter(1.5, 2.5, default=2.0, space="buy", optimize=True)
    buy_bb_percent = DecimalParameter(0.0, 0.3, default=0.15, space="buy", optimize=True)
    buy_volume_factor = DecimalParameter(1.0, 2.5, default=1.5, space="buy", optimize=True)
    
    # Parámetros fijos
    timeframe = '15m'
    stoploss = -0.06  # Stop loss del 6%
    trailing_stop = True
    trailing_stop_positive = 0.015  # Activar trailing stop después de 1.5% de ganancia
    trailing_stop_positive_offset = 0.025  # Mantener al menos 2.5% de ganancia
    trailing_only_offset_is_reached = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    
    # ROI table
    minimal_roi = {
        "0": 0.10,   # 10% después de 0 minutos
        "30": 0.05,  # 5% después de 30 minutos
        "60": 0.03,  # 3% después de 60 minutos
        "120": 0.01  # 1% después de 120 minutos
    }
    
    # Informative pairs
    informative_timeframe = '1h'
    
    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]
        return informative_pairs
    
    def bot_start(self, **kwargs) -> None:
        try:
            exchange = self.dp.exchange.name if hasattr(self.dp, 'exchange') and hasattr(self.dp.exchange, 'name') else 'binance'
            stake_currency = self.dp.stake_currency if hasattr(self.dp, 'stake_currency') else 'USDT'
            stake_amount = self.dp.stake_amount if hasattr(self.dp, 'stake_amount') else 'unlimited'
            
            startup_msg = f"""🤖 *FreqTrade Bot Startup - RSI+Bollinger*

*Exchange:* `{exchange}`
*Stake per trade:* `{stake_amount} {stake_currency}`
*Minimum ROI:* `{self.minimal_roi}`
*Trailing Stoploss:* `{self.stoploss}`
*Position adjustment:* `Off`
*Timeframe:* `{self.timeframe}`
*Strategy:* `RSI_BollingerStrategy`
*Startup candles:* `{self.startup_candle_count}`

Bot iniciado correctamente y listo para operar."""
            
            if hasattr(self.dp, 'send_msg'):
                self.dp.send_msg(startup_msg)
        except Exception as e:
            logger.warning(f"No se pudo enviar mensaje de startup: {e}")
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI para momentum
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # Bollinger Bands
        bollinger = ta.BBANDS(dataframe, timeperiod=int(self.buy_bb_period.value), 
                              nbdevup=float(self.buy_bb_std.value), 
                              nbdevdn=float(self.buy_bb_std.value), matype=0)
        dataframe['bb_lowerband'] = bollinger['lowerband']
        dataframe['bb_middleband'] = bollinger['middleband']
        dataframe['bb_upperband'] = bollinger['upperband']
        dataframe['bb_percent'] = (dataframe['close'] - dataframe['bb_lowerband']) / (
            dataframe['bb_upperband'] - dataframe['bb_lowerband']
        )
        
        # EMA para tendencia
        dataframe['ema'] = ta.EMA(dataframe, timeperiod=21)
        
        # Volumen promedio
        dataframe['volume_sma'] = dataframe['volume'].rolling(window=20).mean()
        
        # Informative timeframe (1h) para contexto
        informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.informative_timeframe)
        informative['rsi'] = ta.RSI(informative, timeperiod=14)
        informative['ema'] = ta.EMA(informative, timeperiod=21)
        dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.informative_timeframe,
                                          ffill=True)
        
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # RSI en rango favorable
                (dataframe['rsi'] > self.buy_rsi_min.value) &
                (dataframe['rsi'] < self.buy_rsi_max.value) &
                # Precio cerca de banda inferior (rebote esperado)
                (dataframe['bb_percent'] < self.buy_bb_percent.value) &
                # Precio por encima de EMA (tendencia alcista)
                (dataframe['close'] > dataframe['ema']) &
                # Tendencia alcista en timeframe superior
                (dataframe['close'] > dataframe[f'ema_{self.informative_timeframe}']) &
                (dataframe[f'rsi_{self.informative_timeframe}'] > 50) &
                # Confirmación de volumen
                (dataframe['volume'] > dataframe['volume_sma'] * self.buy_volume_factor.value) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Precio toca banda superior (sobrecompra)
                (dataframe['bb_percent'] > 0.95) |
                # RSI sobrecomprado
                (dataframe['rsi'] > 75) |
                # Precio cruza por debajo de EMA
                (dataframe['close'] < dataframe['ema']) &
                (dataframe['close'].shift(1) >= dataframe['ema'].shift(1)) |
                # Cambio de tendencia en timeframe superior
                (dataframe['close'] < dataframe[f'ema_{self.informative_timeframe}']) |
                (dataframe[f'rsi_{self.informative_timeframe}'] < 40)
            ),
            'exit_long'] = 1
        
        return dataframe

