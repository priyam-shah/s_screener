from typing_extensions import Self
import numpy as np # for numerical computing
import pandas as pd
from pandas.core import series # for data scirnce
from scipy import stats
from statistics import mean

import streamlit as st

import requests # HTTP requests

import sys

import math

import config

class recoClass:
    
    def ewifunc(self, aumvalue):
        stocks = pd.read_csv('resources/stocks_us-sp-500.csv')

        def chunks(all_stocks, n):
            # all_stocks here is a pandas series
            for i in range(0, len(all_stocks), n):
                # Yield successive n-sized chunks from all_stocks -> ie 5 pandas series will be returned
                yield all_stocks[i: i+n]

        stock_grp =  list(chunks(stocks['Security Name'], 100))

        stock_list = []

        for i in range(0, len(stock_grp)):
            stock_list.append(','.join(stock_grp[i]))


        # ***note*** 
        # looping through pandas DataFrame: stock_list
        # fetching required data using batch api call: api_data from batch_api_call_url 
        # storing it back to DataFrame: stock_dataframe 

        req_columns = [ 'Symbol', 'CMP', 'MCap', 'QUANTITY']

        stock_dataframe = pd.DataFrame(columns = req_columns)


        try:
            for stock_list in stock_list:
                batch_api_call_url = f"https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={stock_list}&token={config.IEX_API_KEY}"
                api_data = requests.get(batch_api_call_url).json()

                for stock in stock_list.split(','):
                    stock_dataframe = stock_dataframe.append(
                                                            pd.Series(
                                                            [
                                                                stock,
                                                                api_data[stock]['quote']['latestPrice'],
                                                                api_data[stock]['quote']['marketCap'],
                                                                'no data'
                                                            ],
                                                            index= req_columns
                                                            ),
                                                            ignore_index=True
                                                            )
        except KeyError as e:
            print ('I got an KeyError - reason', {str(e)})

        # ***note***
        # updating DataFrame with no of stocks to buy for equal weight index fund

        # aum = input("(Value comming from frontend) aum:")
        # aum = str(sys.argv[1])
        
        aumtup = aumvalue
        aum = ' '
        for item in aumtup:
            aum = aum + item

        try:
            val = float(aum)
        except ValueError:
            print("Not a Number\n try again:")
            # aum = input("(Value comming from frontend) aum:")

        no_of_stocks = len(stock_dataframe.index)

        holding_amt_per_stock = float(aum) / no_of_stocks

        for i in range(0, len(stock_dataframe['Symbol'])):
            stock_dataframe.loc[i, 'QUANTITY'] = math.floor(holding_amt_per_stock / stock_dataframe['CMP'][i])

        return stock_dataframe

    def qmsfunc(self, aumvalue):
        stocks = pd.read_csv('/Users/priyamshah/Desktop/algoside-trade/py-script/resources/stocks_us-sp-500.csv')

        def chunks(all_stocks, n):
            # all_stocks here is a pandas series
            for i in range(0, len(all_stocks), n):
                # Yield successive n-sized chunks from all_stocks -> ie 5 pandas series will be returned
                yield all_stocks[i: i+n]

        stock_grp =  list(chunks(stocks['Security Name'], 100))

            # stock_list = []

        pm_stock_list = []

            # for i in range(0, len(stock_grp)):
            #     stock_list.append(','.join(stock_grp[i]))

        for i in range(0, len(stock_grp)):
            pm_stock_list.append(','.join(stock_grp[i]))    

        # ***note***
        # looping through pandas DataFrame: stock_list
        # fetching required data using batch api call: api_data from batch_api_call_url 
        # storing it back to DataFrame: stock_dataframe  

            # req_columns = [ 'Symbol', 'CMP', '% P&L', 'QUANTITY']

            # stock_dataframe = pd.DataFrame(columns = req_columns)

            # for stock_list in stock_list:
            #     batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={stock_list}&token={secrets.IEX_API_KEY}'
            #     api_data = requests.get(batch_api_call_url).json()
                
            #     for stock in stock_list.split(','):
            #         stock_dataframe = stock_dataframe.append(
            #                                                     pd.Series(
            #                                                     [
            #                                                         stock,
            #                                                         api_data[stock]['quote']['latestPrice'],
            #                                                         api_data[stock]['stats']['year1ChangePercent'],
            #                                                         'no data'
            #                                                     ],
            #                                                     index= req_columns
            #                                                     ),
            #                                                     ignore_index=True
            #                                                     )

        # ***note***
        # filtering 50 stocks with highest momentum (1 year)

            # stock_dataframe.sort_values('% P&L', ascending=False, inplace=True)

            # stock_dataframe = stock_dataframe[:50]
            # stock_dataframe.reset_index(drop=True, inplace=True)

        # ***note***
        # updating DataFrame with no of stocks to buy (aum eqully divided btw all the stocks)

        aumtup = aumvalue
        aum = ' '
        for item in aumtup:
            aum = aum + item

        def aumsize_input():
            # global aum
            # aum = str(sys.argv[1])
            # aum = input("(Value comming from frontend) aum:")
            # print(aum)

            try:
                val = float(aum)
            except ValueError:
                print("Not a Number\n try again:")
                # aum = input("(Value comming from frontend) aum:")

            # aumsize_input()

            # no_of_stocks = len(stock_dataframe.index)

            # holding_amt_per_stock = float(aum) / no_of_stocks

            # for i in range(0, len(stock_dataframe['Symbol'])):
            #     stock_dataframe.loc[i, 'QUANTITY'] = math.floor(holding_amt_per_stock / stock_dataframe['CMP'][i])


        # ***note***
        # -- enhanced version -- 

        # ***note***
        # looping through pandas DataFrame: pm_stock_list
        # fetching required data using batch api call: api_data from batch_api_call_url 
        # storing it back to DataFrame: pm_stock_dataframe
        # calculating and storing: percentile scores and avg of percentiles for the stocks

        pm_req_columns = [
            'Symbol', 
            'CMP', 
            'QUANTITY',
            '% P&L 1Y',
            'PCTL P&L 1Y',
            '% P&L 6M',
            'PCTL P&L 6M',
            '% P&L 3M',
            'PCTL P&L 3M',
            '% P&L 1M',
            'PCTL P&L 1M',
            'AVG score'
        ]

        pm_stock_dataframe = pd.DataFrame(columns= pm_req_columns)

        for stock_list in pm_stock_list:
            batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={stock_list}&token={config.IEX_API_KEY}'
            api_data = requests.get(batch_api_call_url).json()

            for stock in stock_list.split(','):
                pm_stock_dataframe = pm_stock_dataframe.append(
                                                                pd.Series(
                                                                [
                                                                    stock,
                                                                    api_data[stock]['quote']['latestPrice'],
                                                                    'no data',
                                                                    api_data[stock]['stats']['year1ChangePercent'],
                                                                    'no data',
                                                                    api_data[stock]['stats']['month6ChangePercent'],
                                                                    'no data',
                                                                    api_data[stock]['stats']['month3ChangePercent'],
                                                                    'no data',
                                                                    api_data[stock]['stats']['month1ChangePercent'],
                                                                    'no data',
                                                                    'no data'
                                                                ],
                                                                index= pm_req_columns
                                                                ),
                                                                ignore_index=True
                                                                )

        parameters = ['1Y', '6M', '3M', '1M']


        for row in pm_stock_dataframe.index:
            for time in parameters:
                if(pm_stock_dataframe.loc[row, f'% P&L {time}'] == None):
                    # print(f'TypeError NoneType encountered at {row} {time}')
                    pm_stock_dataframe.loc[row, f'% P&L {time}'] = -99.0
                    
        for row in pm_stock_dataframe.index:
            for time in parameters:
                # print(pm_stock_dataframe.loc[row, f'% P&L {time}'])
                pm_stock_dataframe.loc[row, f'PCTL P&L {time}'] = stats.percentileofscore(pm_stock_dataframe[f'% P&L {time}'], pm_stock_dataframe.loc[row, f'% P&L {time}'])/100

        for row in pm_stock_dataframe.index:
            avg_pctl = []
            for time in parameters:
                avg_pctl.append(pm_stock_dataframe.loc[row, f'PCTL P&L {time}'])
            pm_stock_dataframe.loc[row, 'AVG score'] = mean(avg_pctl)
            

        # ***note***
        # filtering 50 stocks with "persistent momentum" stocks (consistent in returns)

        pm_stock_dataframe.sort_values('AVG score', ascending=False, inplace=True)

        pm_stock_dataframe = pm_stock_dataframe[:50]
        pm_stock_dataframe.reset_index(drop=True, inplace=True)

        aumsize_input()

        no_of_stocks = len(pm_stock_dataframe.index)

        holding_amt_per_stock = float(aum) / no_of_stocks

        for i in range(0, len(pm_stock_dataframe['Symbol'])):
            pm_stock_dataframe.loc[i, 'QUANTITY'] = math.floor(holding_amt_per_stock / pm_stock_dataframe['CMP'][i])

        return pm_stock_dataframe
