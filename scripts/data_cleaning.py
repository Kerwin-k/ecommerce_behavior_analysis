# scripts/data_cleaning.py

import pandas as pd
import os

def load_raw_data():
    # 构造原始数据路径
    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'online_retail_raw.csv')
    # 读取 CSV
    df = pd.read_csv(raw_path, encoding='ISO-8859-1')

    print("Shape:", df.shape) # 数据形状
    print("Columns：", df.columns.tolist()) # 列名
    print("Sample data:\n", df.head()) # 前 5 条样例:
    return df

if __name__ == "__main__":
    df_raw = load_raw_data()
