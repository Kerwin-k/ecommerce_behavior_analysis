# scripts/feature_engineering.py

import pandas as pd
import os
import datetime as dt


def load_cleaned_data():
    """从 processed 文件夹加载清洗后的数据"""
    processed_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'online_retail_cleaned.csv')

    # 在读取时直接将 InvoiceDate 列解析为日期格式，效率更高
    df = pd.read_csv(processed_path, parse_dates=['InvoiceDate'])

    print("已成功加载清洗后的数据。")
    print("数据形状:", df.shape)
    print("数据样例:\n", df.head())
    return df


def calculate_rfm(df):
    """计算每个客户的 RFM 指标"""
    # 1. 计算每笔交易的总价
    df['TotalPrice'] = df['Quantity'] * df['Price']
    print("\n已创建 'TotalPrice' 列。")

    # 2. 确定用于计算 Recency 的“快照日期”
    # 我们不能用今天的日期，因为数据集是历史数据。
    # 最好的方法是取数据中最新日期的后一天作为基准。
    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    print(f"RFM分析的基准日期 (Snapshot Date): {snapshot_date.date()}")

    # 3. 按 Customer ID 聚合数据，计算 RFM 指标
    print("开始按客户ID聚合，计算R, F, M值...")
    rfm_data = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda date: (snapshot_date - date.max()).days,  # Recency: 计算基准日期与最近一次购买日期的天数差
        'Invoice': 'nunique',  # Frequency: 计算不重复的订单数量
        'TotalPrice': 'sum'  # Monetary: 计算消费总金额
    })

    # 4. 重命名列名
    rfm_data.rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency',
        'TotalPrice': 'Monetary'
    }, inplace=True)

    print("RFM 指标计算完成！")
    print("RFM 数据样例:\n", rfm_data.head())

    return rfm_data


def save_rfm_data(df_rfm):
    """将 RFM 数据保存到 processed 文件夹"""
    rfm_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'rfm_data.csv')
    df_rfm.to_csv(rfm_path, index=True)  # 这里我们保留索引，因为 Customer ID 就是索引
    print(f"\nRFM 数据已成功保存至: {rfm_path}")


if __name__ == "__main__":
    # 步骤1: 加载清洗后的数据
    print("--- 特征工程脚本开始 ---")
    df_cleaned = load_cleaned_data()

    # 步骤2: 计算 RFM 指标
    df_rfm = calculate_rfm(df_cleaned)

    # 步骤3: 保存 RFM 结果
    save_rfm_data(df_rfm)

    print("\n--- 特征工程脚本运行结束 ---")