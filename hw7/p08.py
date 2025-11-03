# p08.py
# Oscar Silva-Santiago

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def bar_plot(df: pd.DataFrame, subcategory: str):
    # aggregate the units sold for each month in 2019
    # produce bar plot and return the 'axes'
    df_subcategory = df[df['SubCategory'] == subcategory]
    df_subcategory['Month Sold'] = pd.to_datetime(df_subcategory['Month Sold'], format='%y-%b')
    print(df_subcategory)
    ax = 1
    return ax


def bars_plot(df: pd.DataFrame, starts_with: str):
    # include all subcategories that start with <starts_with>
    # aggregate the units sold for each month in 2019
    # produce a column of subplots each containing a bar plot
    # return the 'axes'
    ax = 1
    return ax

def main_bar():
    subcategory = input('Enter SubCategory: ')
    df = pd.read_csv('food_cleaned.csv')
    bar_plot(df, subcategory)
    # plt.show()


def main_bars():
    starts_with = input('Enter starts-with phrase: ')
    df = pd.read_csv('food_cleaned.csv')
    # bars_plot(df, starts_with)
    # plt.show()

if __name__ == '__main__':
    main_bar()