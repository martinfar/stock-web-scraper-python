from finvizfinance.screener.custom import Custom
import json
import pandas as pd
import logging

foverview = Custom()


def custom_screener (filters_dict=None):
    foverview.set_filter(filters_dict=filters_dict)
    df = foverview.screener_view()
    tickers_list = df['Ticker'].to_list()
    return tickers_list