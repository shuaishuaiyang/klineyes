#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec

from klineyes.markets.stocks.kline_data import kline_data

# print kline_data.get_basic_data(ktype='30', code='000001', start='2016-04-11', end='2016-06-12')
# 300181 300121
df = kline_data.get_indicator(ktype='30', code='300181', start='2016-04-01', end='2016-06-17', indicator=['MACD'])

# print df[df.macdhist == df[df.macd_shape == 'golden'].macdhist.min()]
golden_intersections = df[(df.macd_shape == 'golden')].reset_index(drop=True)
zero_intersections = df[(df.macd_shape == 'inc_touch_zero')].reset_index(drop=True)
min_point_date = df[(df.macd_shape == 'min_point')].date.values[0]






def get_golden_date(golden_intersections):
    golden_date = None
    zero_points_list = []
    for i, row in golden_intersections.iterrows():
            if dt.timedelta(days=0) < (row.date - min_point_date) <= dt.timedelta(days=1):
                golden_date = row.date
    if golden_date is not None:
        for i, row in zero_intersections.iterrows():
            if (row.date - golden_date) >= dt.timedelta(days=1):
                zero_points_list.append(row.date)
    if len(zero_points_list) > 0:
        return min(zero_points_list)
            # if not next_row.empty:
            #     next_row_shape = next_row.macd_shape.values[0]
            #     if next_row_shape == 'inc_touch_zero':      # DIF在金叉后后面触碰zero
            #         if ((next_row.date - row.date) >= dt.timedelta(days=5)).values[0]:  # 两次形态相差5天以上
            #             range_df = df[(df.date > row.date) & (df.date < next_row.date.values[0])]
            #             print row.date
            #             print price_divergence(range_df)



print get_golden_date(golden_intersections)















def show_plot():

    df['date'] = pd.to_datetime(df.date)
    # 绘图
    fig = plt.figure(figsize=(16, 9))
    gs = GridSpec(3, 1) # 2 rows, 3 columns

    price = fig.add_subplot(gs[:2, 0])
    price.plot(df['date'], df['close'], color='blue')

    indicator = fig.add_subplot(gs[2, 0], sharex=price)
    indicator.plot(df['date'], df['macdsignal'], c='pink')
    indicator.plot(df['date'], df['macd'], c='yellowgreen')
    indicator.plot(df['date'], [0.]*len(df['date']), c='gray')
    # indicator.bar(df['date'],df['macdhist'])#df['macdhist']
    # 划MACD交点
    area = np.pi * 5  # 0 to 15 point radiuses
    indicator.scatter(golden['date'].values, golden['macd'].values,s = area, color='red')
    indicator.scatter(death['date'].values, death['macd'].values,s = area, color='green')
    price.scatter(golden['date'].values, golden['close'].values,s = area, color='red')
    price.scatter(death['date'].values, death['close'].values,s = area, color='green')
    price.grid(True)
    indicator.grid(True)
    plt.tight_layout()
    plt.show()

# show_plot()