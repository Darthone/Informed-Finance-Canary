import bisect
from ifc.stockData import get_data_for_sym
import pandas as pd
import numpy as np
from datetime import datetime

def dicts_to_df(list_of_dicts):
    """ convert data from yahoo finance """
    df = pd.DataFrame(list_of_dicts)
    df.drop('Symbol', axis=1, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date')
    cols = ['High', 'Low', 'Volume', 'Open', 'Close', 'Adj_Close']
    for c in cols:
        df[c] = pd.to_numeric(df[c])
    return df

def get_series(ticker_sym, start, end):
    return Series(dicts_to_df(get_data_for_sym(ticker_sym, start, end)))

class Series(object):
    """ used to represent a series of days """
    def __init__(self, dataframe, config=None):
        self.df = dataframe
        self.max_win = 26
        if config is None: # default settings
            self.mavg = [10, 30]
            self.macd = [(9, 12, 26)]
            self.ema = []
            self.rsi = [14]
        else:
            raise NotImplementedError

    def run_calculations(self):
        """ runs a set of default calculations """ 
        for w in self.mavg:
            self.calculate_mavg(w)
        for w in self.macd:
            self.calculate_macd(w[0], w[1], w[2])
        for w in self.ema:
            self.calculate_ema(w)
        for w in self.rsi:
            self.calculate_rsi(w)

    def set_max_win(self, val):
        self.max_win = val if val > self.max_win else self.max_win

    def trim_fat(self, window=None):
        temp_win = window
        if temp_win is None:
            temp_win = self.max_win
        self.df = self.df[temp_win:] # drop the first n rows typically containing Nan

    def calculate_mavg(self, window=10, col='Adj_Close'):
        """ calculates a simple moving average """
        self.set_max_win(window)
        name = "mavg_%s" % (window)
        self.df[name] = self.df['Adj_Close'].rolling(window=window).mean()

    def calculate_rsi(self, window=14, col='Adj_Close'):
        self.set_max_win(window)
        delta = self.df[col].diff()
        dUp, dDown = delta.copy(), delta.copy()
        dUp[dUp < 0] = 0
        dDown[dDown > 0] = 0
        RolUp = dUp.rolling(window=window).mean()
        RolDown = dDown.rolling(window=window).mean().abs()
        name = "rsi_%s" % (window)
        RS = RolUp / RolDown
        self.df[name] = 100.0 - (100.0 / (1.0 + RS))

    def calculate_ema(self, window, name=None, col='Adj_Close'):
        self.set_max_win(window)
        if name is None:
            name = "ema_%s" % (window)
        self.df[name] = pd.ewma(self.df[col], span=window, min_periods=window)

    def calculate_macd(self, signal=9, fast=12, slow=26, col='Adj_Close'):
        """ MACD """
        self.set_max_win(slow)
        signal_name = "signal_%s" % (signal)
        # ignore warnings for now # TODO
        fast_ema = pd.ewma(self.df[col], span=fast, min_periods=fast)
        slow_ema = pd.ewma(self.df[col], span=slow, min_periods=slow)
        name = "macd_%s_%s" % (fast, slow)
        self.df[name] = fast_ema - slow_ema
        self.calculate_ema(signal, col=name, name=signal_name)

    def calculate_mom(self, col='Adj_Close', window=1):
        """ Momentum Measures the change in price
                Price(t)-Price(t-n)
        """
        self.set_max_win(window)
        name = "mom_%s" % (window)
        self.df[name] = self.df[col] - self.df[col].shift(window)

    def calculate_rocr(self, window=3, col='Adj_Close'):
        """ Rate of Change Compute rate of change 
            relative to previous trading intervals
                (Price(t)/Price(t-n))*100
        """
        self.set_max_win(window)
        name = "rocr_%s" % (window)
        self.df[name] = (self.df[col] / self.df[col].shift(window)) * 100

    def calculate_atr(self, window=14):
        """ Average True Range Shows volatility of market 
                ATR(t) = ((n-1) * ATR(t-1) + Tr(t)) / n 
                where Tr(t) = Max(Abs(High - Low), Abs(High - Close(t - 1)), Abs(Low - Close(t - 1));
        """
        self.set_max_win(window)
        i = 0  
        tr_l = [0]  
        for i in range(self.df.index[-1]):  
            tr = max(self.df.get_value(i + 1, 'High'), 
                     self.df.get_value(i, 'Adj_Close')) - min(self.df.get_value(i + 1, 'Low'), 
                     self.df.get_value(i, 'Adj_Close'))  
            tr_l.append(tr)  
        name = 'atr_%s' % (window)
        self.df[name] = pd.ewma(pd.Series(tr_l), span=window, min_periods=window)

    def calculate_mfi(self, window=14):
        """ Money Flow Index Relates typical price with Volume 
                100 - (100 / (1 + Money Ratio)) 
                where Money Ratio=(+Moneyflow / -Moneyflow);
                Moneyflow=Tp*Volume
                Tp = (High + Low + Close)/3
        """
        name = "mfi_%s" % (window)
        tp = (self.df['High'] + self.df['Low'] + self.df['Adj_Close']) / 3
        i = 0  
        PosMF = [0]  
        while i < self.df.index[-1]:  
            if tp[i + 1] > tp[i]:  
                PosMF.append(tp[i + 1] * self.df.get_value(i + 1, 'Volume'))  
            else:  
                PosMF.append(0)  
            i = i + 1  
        PosMF = pd.Series(PosMF)  
        TotMF = tp * self.df['Volume']  
        MFR = pd.Series(PosMF / TotMF)  
        self.df[name] = MFR.rolling(window=window).mean()

    def calculate_adx(self, window=14, window_adx=14):
        """ Average Directional Index Discover if trend is developing
                Sum((+DI-(-DI))/(+DI+(-DI))/n
        """
        self.set_max_win(window)
        i = 0  
        UpI = []  
        DoI = []  
        while i + 1 <= self.df.index[-1]:  
            UpMove = self.df.get_value(i + 1, 'High') - self.df.get_value(i, 'High')  
            DoMove = self.df.get_value(i, 'Low') - self.df.get_value(i + 1, 'Low')  
            if UpMove > DoMove and UpMove > 0:  
                UpD = UpMove  
            else: UpD = 0  
            UpI.append(UpD)  
            if DoMove > UpMove and DoMove > 0:  
                DoD = DoMove  
            else: DoD = 0  
            DoI.append(DoD)  
            i = i + 1  
        atr_name = "atr_%s" % (window)
        self.calculate_atr(window)
        PosDI = pd.ewma(pd.Series(UpI), span=window, min_periods=window-1) / self.df[atr_name]
        NegDI = pd.ewma(pd.Series(DoI), span=window, min_periods=window-1) / self.df[atr_name]
        name = "adx_%s_%s" % (window, window_adx)
        self.df[name] = pd.Series(pd.ewma(abs(PosDI - NegDI) / (PosDI + NegDI), span=window_adx, min_periods=window_adx-1))

    def calculate_cci(self, window=12):
        """ Commodity Channel Index Identifies cyclical turns in stock price 
                Tp(t) - TpAvg(t,n) / (0.15 * MD(t)) where:
                Tp(t) = (High(t)+Low(t)+Close(t))/3;
                TpAvg(t,n) = Avg(Tp(t)) over [t, t-1, ..., t-n+1];
                MD(t)=Avg(Abs(Tp(t)-TpAvg(t,n)));
        """
        self.set_max_win(window)
        tp = (self.df['High'] + self.df['Low'] + self.df['Adj_Close']) / 3
        name = "cci_%s" % (window)
        self.df[name] = pd.Series((tp - tp.rolling(window=window).mean()) / tp.rolling(window=window, center=False).std())

    def calculate_obv(self, col='Adj_Close', window=14):
        """ On Balance Volume is a momentum indicator that uses volume flow
                OBV(t) = OBV(t-1) +/-Volume(t)
        """
        self.set_max_win(window)
        obv = [0]  
        for i in range(1, len(self.df.index) - 1):  
            if self.df.get_value(i + 1, col) - self.df.get_value(i, col) > 0:  
                obv.append(self.df.get_value(i + 1, 'Volume'))  
            if self.df.get_value(i + 1, col) - self.df.get_value(i, col) == 0:  
                obv.append(0)  
            if self.df.get_value(i + 1, col) - self.df.get_value(i, col) < 0:  
                obv.append(-self.df.get_value(i + 1, 'Volume'))  
        name = "obv_%s" % (window)
        self.df[name] = pd.Series(obv).rolling(window=window).mean()

    def calculate_trix(self, window=15):
        """ Triple Exponential Moving Average Smooth the insignificant movements 
                TR(t) / TR(t-1) where 
                TR(t) = EMA(EMA(EMA(Price(t)))) over n days period
        """
        self.set_max_win(window)
        #ignore produced warnings for now #TODO
        ema = pd.ewma(self.df['Adj_Close'], span=window, min_periods=window-1)
        ema = pd.ewma(ema, span=window, min_periods=window-1)
        ema = pd.ewma(ema, span=window, min_periods=window-1)

        roc_l = [0]  
        for i in range(1, len(self.df.index) - 1):  
            roc_l.append((ema[i + 1] - ema[i]) / ema[i])  

        name = "trix_%s" % (window)
        self.df[name] = pd.Series(roc_l)

