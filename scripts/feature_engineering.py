# scripts/feature_engineering.py

import pandas as pd
import os
import datetime as dt


def load_cleaned_data():
    """从 processed 文件夹加载清洗后的数据"""
    processed_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'online_retail_cleaned.csv')
    df = pd.read_csv(processed_path, parse_dates=['InvoiceDate'])

    print("Cleaned data loaded successfully.")
    print("Data shape:", df.shape)
    print("Data sample:\n", df.head())
    return df


def calculate_rfm(df):
    """计算每个客户的 RFM 指标"""
    df['TotalPrice'] = df['Quantity'] * df['Price']
    print("\n'TotalPrice' column created.")

    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    print(f"Snapshot Date for RFM analysis: {snapshot_date.date()}")

    print("Aggregating by Customer ID to calculate R, F, M values...")
    rfm_data = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda date: (snapshot_date - date.max()).days,
        'Invoice': 'nunique',
        'TotalPrice': 'sum'
    })

    rfm_data.rename(columns={
        'InvoiceDate': 'Recency',
        'Invoice': 'Frequency',
        'TotalPrice': 'Monetary'
    }, inplace=True)

    print("RFM calculation complete!")
    print("RFM data sample:\n", rfm_data.head())

    return rfm_data


def save_rfm_data(df_rfm):
    """将 RFM 数据保存到 processed 文件夹"""
    rfm_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'rfm_data.csv')
    df_rfm.to_csv(rfm_path, index=True)
    print(f"\nRFM data successfully saved to: {rfm_path}")


if __name__ == "__main__":
    print("--- Feature Engineering Script Started ---")
    df_cleaned = load_cleaned_data()

    df_rfm = calculate_rfm(df_cleaned)

    save_rfm_data(df_rfm)

    print("\n--- Feature Engineering Script Finished ---")