"""
generate_data.py
Generates synthetic sales data for the dashboard.
"""

import pandas as pd
import numpy as np
import os

def generate_sales_data(n_records=500, seed=42):
    np.random.seed(seed)

    regions     = ['North', 'South', 'East', 'West']
    categories  = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
    salespersons = ['Alice', 'Bob', 'Carol', 'David', 'Eva', 'Frank']

    dates = pd.date_range(start='2023-01-01', end='2023-12-31', periods=n_records)

    df = pd.DataFrame({
        'date':        dates,
        'region':      np.random.choice(regions, n_records),
        'category':    np.random.choice(categories, n_records),
        'salesperson': np.random.choice(salespersons, n_records),
        'units_sold':  np.random.randint(1, 50, n_records),
        'unit_price':  np.round(np.random.uniform(10, 500, n_records), 2),
        'discount_pct':np.round(np.random.uniform(0, 0.3, n_records), 2),
    })

    df['revenue']      = np.round(df['units_sold'] * df['unit_price'] * (1 - df['discount_pct']), 2)
    df['month']        = df['date'].dt.month_name()
    df['quarter']      = df['date'].dt.to_period('Q').astype(str)

    os.makedirs('../data', exist_ok=True)
    df.to_csv('../data/sales_data.csv', index=False)
    print(f"Sales data saved — {len(df)} records")
    return df


if __name__ == '__main__':
    generate_sales_data()
