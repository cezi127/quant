# -*- coding: utf-8 -*-
#

from functools import reduce

import numpy as np
import math
import talib

from .context import ExecutionContext
from .utils import FormulaException, rolling_window, handle_numpy_warning
from .time_series import (
    MarketDataSeries,
    NumericSeries,
    BoolSeries,
    fit_series,
    get_series,
    get_bars,
    ensure_timeseries,
)

class OneArgumentSeries(NumericSeries):
    def __init__(self, series, arg):
        if isinstance(series, NumericSeries):
            series = series.series

            try:
                series[series == np.inf] = np.nan
                series = eval(self.funcName)(series, arg)
            except Exception as e:
                raise FormulaException(e)
        super(OneArgumentSeries, self).__init__(series)
        self.extra_create_kwargs["arg"] = arg


    @property
    def funcName(self):
        raise NotImplementedError

class MovingAverageSeries(OneArgumentSeries):
#    """http://www.tadoc.org/indicator/MA.htm"""
#    func = talib.MA
    @property
    def funcName(self):
        return 'talib.MA'


class WeightedMovingAverageSeries(OneArgumentSeries):
#    """http://www.tadoc.org/indicator/WMA.htm"""
#    func = talib.WMA
    @property
    def funcName(self):
        return 'talib.WMA'

class ExponentialMovingAverageSeries(OneArgumentSeries):
#    """http://www.fmlabs.com/reference/default.htm?url=ExpMA.htm"""
#    func = talib.EMA
    @property
    def funcName(self):
        return 'talib.EMA'

class StdSeries(OneArgumentSeries):
#    func = talib.STDDEV
    @property
    def funcName(self):
        return 'talib.STDDEV'



class TwoArgumentSeries(NumericSeries):
    func = talib.STDDEV

    def __init__(self, series, arg1, arg2):
        if isinstance(series, NumericSeries):
            series = series.series

            try:
                series[series == np.inf] = np.nan
                series = self.func(series, arg1, arg2)
            except Exception as e:
                raise FormulaException(e)
        super(TwoArgumentSeries, self).__init__(series)
        self.extra_create_kwargs["arg1"] = arg1
        self.extra_create_kwargs["arg2"] = arg2


class SMASeries(TwoArgumentSeries):
    """???????????????SMA"""

    def func(self, series, n, _):
        results = np.nan_to_num(series).copy()
        # FIXME this is very slow
        for i in range(1, len(series)):
            results[i] = ((n - 1) * results[i - 1] + results[i]) / n
        return results


class SumSeries(NumericSeries):
    """??????"""
    def __init__(self, series, period):
        if isinstance(series, NumericSeries):
            series = series.series
            try:
                series[series == np.inf] = 0
                series[series == -np.inf] = 0
                series = talib.SUM(series, period)
            except Exception as e:
                raise FormulaException(e)
        super(SumSeries, self).__init__(series)
        self.extra_create_kwargs["period"] = period


class AbsSeries(NumericSeries):
    def __init__(self, series):
        if isinstance(series, NumericSeries):
            series = series.series
            try:
                series[series == np.inf] = 0
                series[series == -np.inf] = 0
                series = np.abs(series)
            except Exception as e:
                raise FormulaException(e)
        super(AbsSeries, self).__init__(series)


@handle_numpy_warning
def CrossOver(s1, s2):
    """s1??????s2
    :param s1:
    :param s2:
    :returns: bool??????
    :rtype: BoolSeries
    """
    s1, s2 = ensure_timeseries(s1), ensure_timeseries(s2)
    series1, series2 = fit_series(s1.series, s2.series)
    cond1 = series1 > series2
    series1, series2 = fit_series(s1[1].series, s2[1].series)
    cond2 = series1 <= series2  # s1[1].series <= s2[1].series
    cond1, cond2 = fit_series(cond1, cond2)
    s = cond1 & cond2
    return BoolSeries(s)


def Ref(s1, n):
    return s1[n]


@handle_numpy_warning
def minimum(s1, s2):
    s1, s2 = ensure_timeseries(s1), ensure_timeseries(s2)
    if len(s1) == 0 or len(s2) == 0:
        raise FormulaException("minimum size == 0")
    series1, series2 = fit_series(s1.series, s2.series)
    s = np.minimum(series1, series2)
    return NumericSeries(s)


@handle_numpy_warning
def maximum(s1, s2):
    s1, s2 = ensure_timeseries(s1), ensure_timeseries(s2)
    if len(s1) == 0 or len(s2) == 0:
        raise FormulaException("maximum size == 0")
    series1, series2 = fit_series(s1.series, s2.series)
    s = np.maximum(series1, series2)
    return NumericSeries(s)


@handle_numpy_warning
def count(cond, n):
    # TODO lazy compute
    series = cond.series
    size = len(cond.series) - n
    try:
        result = np.full(size, 0, dtype=np.int)
    except ValueError as e:
        raise FormulaException(e)
    for i in range(size - 1, 0, -1):
        s = series[-n:]
        result[i] = len(s[s == True])
        series = series[:-1]
    return NumericSeries(result)


@handle_numpy_warning
def every(cond, n):
    return count(cond, n) == n


@handle_numpy_warning
def hhv(s, n):
    # TODO lazy compute
    series = s.series
    size = len(s.series) - n
    try:
        result = np.full(size, 0, dtype=np.float64)
    except ValueError as e:
        raise FormulaException(e)

    result = np.max(rolling_window(series, n), 1)

    return NumericSeries(result)


@handle_numpy_warning
def llv(s, n):
    # TODO lazy compute
    series = s.series
    size = len(s.series) - n
    try:
        result = np.full(size, 0, dtype=np.float64)
    except ValueError as e:
        raise FormulaException(e)

    result = np.min(rolling_window(series, n), 1)

    return NumericSeries(result)


@handle_numpy_warning
def iif(condition, true_statement, false_statement):
    series1 = get_series(true_statement)
    series2 = get_series(false_statement)
    cond_series, series1, series2 = fit_series(condition.series, series1, series2)

    series = series2.copy()
    series[cond_series] = series1[cond_series]

    return NumericSeries(series)

@handle_numpy_warning
def barslast(cond):
    cond = get_series(cond)
    wz=[]
    nn=[] #np.full(len(cond), 0, dtype=np.int)
    wzn=[]
    rn=[]#barslast(ref(sc))
    for i in list(range(len(cond))):
        if i==0:
            wz.append(0)
        else:
            if cond[i]==True:
                wz.append(i)
            else:
                wz.append(wz[-1])
        n0=i-wz[-1]
        nn.append(n0)
        
        #?????????barslast(ref(sc))
        if i==0:
            wzn.append(0)
        else:
            if wz[i]!=wz[i-1]:
                wzn.append(wz[i-1])
            else:
                wzn.append(wzn[-1])
        rn0=i-wzn[-1]
        rn.append(rn0)
    return nn

@handle_numpy_warning
def filters(A, N):
    BUY = A.series
    #print(BUY)
    BUYsignal = 0
    for i in range(len(BUY)):
        if (BUYsignal > N):
            BUYsignal = 0

        if ((BUY[i] == True) and (BUYsignal == 0)):
            BUYsignal = BUYsignal + 1
        elif (BUYsignal > 0):
            BUY[i] = False
            BUYsignal = BUYsignal + 1
        #print(BUYsignal)
    return BUY

@handle_numpy_warning
def log(cond):
    cond = cond.series
    result = np.log(cond)
    return NumericSeries(result)

@handle_numpy_warning
def floor(cond):
    cond = cond.series
    result = np.floor(cond)
    return NumericSeries(result)

@handle_numpy_warning
def power(n, cond):
    cond = cond.series
    result = np.power(cond, n)
    return NumericSeries(result)