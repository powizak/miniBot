# Conditional import for TA-Lib (production) and pandas-ta (testing)
try:
    import talib
    TA_LIB_AVAILABLE = True
except ImportError:
    import numpy as np
    np.NaN = np.nan  # Patch for pandas-ta compatibility with numpy >= 1.24
    import pandas_ta as ta
    TA_LIB_AVAILABLE = False
import numpy as np
import pandas as pd
# Import talib only if available; otherwise use pandas-ta via TA_LIB_AVAILABLE

from backend.model import ts_model

class Strategy:
    def __init__(self, stop_loss_pct=0.03, max_positions=3, panic_volatility=0.08):
        self.stop_loss_pct = stop_loss_pct
        self.max_positions = max_positions
        self.panic_volatility = panic_volatility
        self.panic_mode = False

    def predict_next_price(self, df):
        """
        Skeleton: Využije ML model pro predikci další ceny.
        """
        # Příklad: použij posledních N hodnot pro predikci
        if len(df) < 1:
            return None
        X = df['close'].values[-1:].reshape(-1, 1)
        pred = ts_model.predict(X)
        return float(pred[0]) if len(pred) > 0 else None

    def compute_indicators(self, df):
        """Přidá do df sloupce s RSI, MACD, BB, MA."""
        if TA_LIB_AVAILABLE:
            df['rsi'] = talib.RSI(df['close'], timeperiod=14)
            macd, macdsignal, macdhist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
            df['macd'] = macd
            df['macdsignal'] = macdsignal
            df['macdhist'] = macdhist
            upper, middle, lower = talib.BBANDS(df['close'], timeperiod=20)
            df['bb_upper'] = upper
            df['bb_middle'] = middle
            df['bb_lower'] = lower
            df['ma'] = talib.SMA(df['close'], timeperiod=20)
        else:
            df['rsi'] = ta.rsi(df['close'], length=14)
            macd = ta.macd(df['close'])
            df['macd'] = macd['MACD_12_26_9']
            df['macdsignal'] = macd['MACDs_12_26_9']
            df['macdhist'] = macd['MACDh_12_26_9']
            bb = ta.bbands(df['close'], length=20)
            df['bb_upper'] = bb['BBU_20_2.0']
            df['bb_middle'] = bb['BBM_20_2.0']
            df['bb_lower'] = bb['BBL_20_2.0']
            df['ma'] = ta.sma(df['close'], length=20)
        return df

    def check_stop_loss(self, entry_price, current_price):
        """Vrací True, pokud je dosažen stop-loss."""
        return current_price <= entry_price * (1 - self.stop_loss_pct)

    def can_open_position(self, open_positions):
        """Vrací True, pokud lze otevřít další pozici."""
        return open_positions < self.max_positions

    def check_panic_mode(self, df):
        """Aktivuje panic režim při extrémní volatilitě."""
        returns = df['close'].pct_change().dropna()
        volatility = returns.rolling(window=10).std().iloc[-1]
        if volatility is not None and volatility > self.panic_volatility:
            self.panic_mode = True
        else:
            self.panic_mode = False
        return self.panic_mode