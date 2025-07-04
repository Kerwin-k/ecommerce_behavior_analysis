# scripts/data_cleaning.py

import pandas as pd
import os

def load_raw_data():
    """
    构造原始数据路径
    """
    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'online_retail_II.csv')
    # 读取 CSV
    df = pd.read_csv(raw_path, encoding='ISO-8859-1')

    print("Shape:", df.shape) # 数据形状
    print("Columns：", df.columns.tolist()) # 列名
    print("Sample data:\n", df.head()) # 前 5 条样例:
    return df

def clean_data(df):
    """
    清洗数据，包括处理缺失值、退货、数据类型转换等。
    """
    # 创建一个副本以避免后续操作出现警告
    df_clean = df.copy()

    # --- 关键步骤1: 处理缺失的 Customer ID ---
    # 没有顾客ID的记录对于客户分析是无用的，必须删除
    print(f"清洗前 'Customer ID' 缺失的数量: {df_clean['Customer ID'].isnull().sum()}")
    df_clean.dropna(subset=['Customer ID'], inplace=True)
    print(f"清洗后 'Customer ID' 缺失的数量: {df_clean['Customer ID'].isnull().sum()}")

    # --- 关键步骤2: 处理退货数据 ---
    # 数量为负数通常代表退货，在计算销售额时不应包含
    initial_rows = len(df_clean)
    df_clean = df_clean[df_clean['Quantity'] > 0]
    print(f"移除退货记录后，行数从 {initial_rows} 变为 {len(df_clean)}。")

    # --- 关键步骤3: 处理价格为0的数据 ---
    # 价格为0的商品通常是赠品或异常数据
    initial_rows = len(df_clean)
    df_clean = df_clean[df_clean['Price'] > 0]
    print(f"移除0元单价记录后，行数从 {initial_rows} 变为 {len(df_clean)}。")

    # (这部分代码仍然是在 clean_data 函数内部，接着上面的代码继续写)

    # --- 关键步骤4: 转换数据类型 ---
    # 将 Customer ID 转换为整数
    df_clean['Customer ID'] = df_clean['Customer ID'].astype(int)
    # 将 InvoiceDate 转换为日期时间格式，为后续分析做准备
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    print("已将 'Customer ID' 转换为整数，'InvoiceDate' 转换为日期时间类型。")

    # --- 关键步骤5: 处理重复记录 ---
    dup_count = df_clean.duplicated().sum()
    print(f"清洗前存在 {dup_count} 条重复记录。")
    if dup_count > 0:
        df_clean.drop_duplicates(inplace=True)
        print(f"移除重复记录后，剩余行数: {len(df_clean)}")

    print("\n数据清洗完成！最终数据信息如下：")
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

    print(f"\n清洗后的数据已成功保存至: {processed_path}")

if __name__ == "__main__":
    # 1. 加载原始数据
    print("--- 步骤1: 开始加载原始数据 ---")
    df_raw = load_raw_data()

    # 2. 清洗数据
    print("\n--- 步骤2: 开始数据清洗 ---")
    df_cleaned = clean_data(df_raw)

    # 3. 保存清洗后的数据
    print("\n--- 步骤3: 开始保存处理后数据 ---")
    save_processed_data(df_cleaned)