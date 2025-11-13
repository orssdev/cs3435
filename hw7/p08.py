# p08.py
# Oscar Silva-Santiago

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def bar_plot(df: pd.DataFrame, subcategory: str):
    # aggregate the units sold for each month in 2019
    # produce bar plot and return the 'axes'
    df['Month Sold'] = pd.to_datetime(df['Month Sold'], format='%y-%b', errors='coerce')
    df_sub = df[df['SubCategory'] == subcategory]
    df_sub = df_sub[df_sub['Month Sold'].dt.year == 2019]

    if df_sub.empty:
        return None

    if 'Unit' in df_sub.columns:
        unit_name = df_sub['Unit'].iloc[0]
    elif 'Units' in df_sub.columns:
        unit_name = df_sub['Units'].iloc[0]
    else:
        unit_name = 'units'

    monthly_sales = df_sub.groupby(df_sub['Month Sold'].dt.to_period('M'))['Units Sold'].sum()

    all_months = pd.period_range(start='2019-01', end='2019-12', freq='M')
    monthly_sales = monthly_sales.reindex(all_months, fill_value=0)
    monthly_sales = monthly_sales.sort_index()

    _ , ax = plt.subplots(figsize=(10, 6))
    monthly_sales.index = monthly_sales.index.to_timestamp()
    monthly_sales.plot(kind='bar', ax=ax)

    month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticklabels(month_abbr, rotation=45)
    ax.set_title(f"{unit_name} — {subcategory}")
    ax.set_xlabel("Month")
    ax.set_ylabel("Units Sold")

    total_units = monthly_sales.sum()
    if total_units > 0:
        weights = np.arange(1, 13)
        avg_month_num = int(round(np.dot(weights, monthly_sales.values) / total_units))
        if 1 <= avg_month_num <= 12:
            avg_month_name = month_abbr[avg_month_num - 1]
            ax.text(0.5, 0.9, f"Average Month: {avg_month_name}",
                    transform=ax.transAxes, fontsize=12, color='darkred',
                    ha='center', va='center')
    plt.tight_layout()
    return ax


def bars_plot(df: pd.DataFrame, starts_with: str):
    # include all subcategories that start with <starts_with>
    # aggregate the units sold for each month in 2019
    # produce a column of subplots each containing a bar plot
    # return the 'axes'
    df['Month Sold'] = pd.to_datetime(df['Month Sold'], format='%y-%b', errors='coerce')
    df = df[df['SubCategory'].str.startswith(starts_with, na=False)]
    df = df[df['Month Sold'].dt.year == 2019]
    grouped = df.groupby([df['SubCategory'], df['Month Sold'].dt.to_period('M')])['Units Sold'].sum()
    all_months = pd.period_range(start='2019-01', end='2019-12', freq='M')

    subcats = sorted(grouped.index.get_level_values(0).unique())
    avg_months = {}

    for sub in subcats:
        vals = grouped[sub].reindex(all_months, fill_value=0)
        vals = vals.sort_index()
        total = vals.sum()
        if total > 0:
            weights = np.arange(1, 13)
            avg_month = np.dot(weights, vals.values) / total
        else:
            avg_month = 0
        avg_months[sub] = avg_month

    subcats = [s for s, _ in sorted(avg_months.items(), key=lambda x: x[1])]
    colors = plt.cm.tab10(np.linspace(0, 1, len(subcats)))
    _ , ax = plt.subplots(len(subcats), 1, figsize=(10, 4*len(subcats)), sharex=True)
    if len(subcats) == 1:
        ax = [ax]

    month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for i, sub in enumerate(subcats):
        vals = grouped[sub].reindex(all_months, fill_value=0)
        vals = vals.sort_index()
        vals.index = vals.index.to_timestamp()
        vals.plot(kind='bar', ax=ax[i], color=colors[i])

        if ax[i].legend_ is not None:
            ax[i].legend_.remove()

        ax[i].text(0.01, 0.9, sub, transform=ax[i].transAxes, ha='left', va='center', fontsize=11)

        total = vals.sum()
        if total > 0:
            weights = np.arange(1, 13)
            avg_month_num = int(round(np.dot(weights, vals.values) / total))
            if 1 <= avg_month_num <= 12:
                avg_name = month_abbr[avg_month_num - 1]
                ax[i].text(0.01, 0.8, f"Average Month: {avg_name}",
                           transform=ax[i].transAxes, ha='left', va='center',
                           fontsize=10, color='darkred')

        if i == 0:
            ax[i].set_title(f'Subcategories starting with "{starts_with}"')
        ax[i].set_ylabel('Units Sold')

    ax[-1].set_xlabel('Month')
    ax[-1].set_xticklabels(month_abbr, rotation=45)
    plt.tight_layout()
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