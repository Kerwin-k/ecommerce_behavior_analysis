# scripts/churn_label.py

import pandas as pd
import os


def load_segment_data():
    """从 processed 文件夹加载分层后的客户数据"""
    segments_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'customer_segments.csv')
    df = pd.read_csv(segments_path)

    print("Customer segment data loaded successfully.")
    print("Data shape:", df.shape)
    print("Data sample:\n", df.head())
    return df


def create_churn_label(df):
    """根据客户分层创建'是否流失'的标签"""
    # 定义哪些分层属于“流失” (使用英文标签)
    churn_segments = ['At Risk', 'Hibernating']

    df['Churn'] = df['Segment'].isin(churn_segments).astype(int)

    print("\n'Churn' label column created.")
    print("Distribution of Churned (1) vs. Active (0) customers:")
    print(df['Churn'].value_counts())

    print("\nData sample with labels:\n", df.head())
    return df


def save_labeled_data(df):
    """将带有流失标签的数据保存到 processed 文件夹"""
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'churn_data.csv')
    df.to_csv(output_path, index=False)
    print(f"\nData with churn labels successfully saved to: {output_path}")


if __name__ == "__main__":
    print("--- Churn Labeling Script Started ---")

    df_segments = load_segment_data()

    df_labeled = create_churn_label(df_segments)

    save_labeled_data(df_labeled)

    print("\n--- Churn Labeling Script Finished ---")