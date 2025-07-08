# scripts/data_cleaning.py

import pandas as pd
import os


def load_raw_data():
    # 构造原始数据路径
    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'online_retail_II.csv')
    # 读取 CSV
    df = pd.read_csv(raw_path, encoding='ISO-8859-1')

    print("Raw data shape:", df.shape)  # 数据形状
    print("Column names:", df.columns.tolist())  # 列名
    print("Raw data sample:\n", df.head())  # 前 5 条样例:
    return df


def clean_data(df):
    """
    清洗数据，包括处理缺失值、退货、数据类型转换等。
    """
    # 创建一个副本以避免后续操作出现警告
    df_clean = df.copy()

    # --- 关键步骤1: 处理缺失的 Customer ID ---
    print(f"\nMissing 'Customer ID' before cleaning: {df_clean['Customer ID'].isnull().sum()}")
    df_clean.dropna(subset=['Customer ID'], inplace=True)
    print(f"Missing 'Customer ID' after cleaning: {df_clean['Customer ID'].isnull().sum()}")

    # --- 关键步骤2: 处理退货数据 ---
    initial_rows = len(df_clean)
    df_clean = df_clean[df_clean['Quantity'] > 0]
    print(f"Removed return records. Row count changed from {initial_rows} to {len(df_clean)}.")

    # --- 关键步骤3: 处理价格为0的数据 ---
    initial_rows = len(df_clean)
    df_clean = df_clean[df_clean['Price'] > 0]
    print(f"Removed zero-price records. Row count changed from {initial_rows} to {len(df_clean)}.")

    # --- 关键步骤4: 转换数据类型 ---
    df_clean['Customer ID'] = df_clean['Customer ID'].astype(int)
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    print("\nConverted 'Customer ID' to integer and 'InvoiceDate' to datetime.")

    # --- 关键步骤5: 处理重复记录 ---
    dup_count = df_clean.duplicated().sum()
    print(f"Found {dup_count} duplicate records before cleaning.")
    if dup_count > 0:
        df_clean.drop_duplicates(inplace=True)
        print(f"Removed duplicates. Final row count: {len(df_clean)}")

    print("\nData cleaning complete! Final data info:")
    df_clean.info()

    return df_clean


def save_processed_data(df, filename="online_retail_cleaned.csv"):
    """
    将处理后的数据保存到 data/processed 目录。
    """
    # 构造保存路径
    processed_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', filename)

    # 使用 to_csv 保存，index=False 表示不把 DataFrame 的索引写入到文件中
    df.to_csv(processed_path, index=False)

    print(f"\nCleaned data successfully saved to: {processed_path}")


if __name__ == "__main__":
    # 1. 加载原始数据
    print("--- Step 1: Loading Raw Data ---")
    df_raw = load_raw_data()

    # 2. 清洗数据
    print("\n--- Step 2: Cleaning Data ---")
    df_cleaned = clean_data(df_raw)

    # 3. 保存清洗后的数据
    print("\n--- Step 3: Saving Processed Data ---")
    save_processed_data(df_cleaned)