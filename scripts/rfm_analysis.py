# scripts/rfm_analysis.py

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def load_rfm_data():
    """从 processed 文件夹加载 RFM 数据"""
    rfm_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'rfm_data.csv')
    df_rfm = pd.read_csv(rfm_path)

    if 'Invoice' in df_rfm.columns:
        df_rfm.rename(columns={'Invoice': 'Frequency'}, inplace=True)

    print("RFM data loaded successfully.")
    print("Data shape:", df_rfm.shape)
    print("Data sample:\n", df_rfm.head())
    return df_rfm


def calculate_scores_and_segments(df_rfm):
    """计算RFM分数，并根据分数进行客户分层"""
    df_rfm['R_Score'] = pd.qcut(df_rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
    df_rfm['F_Score'] = pd.qcut(df_rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    df_rfm['M_Score'] = pd.qcut(df_rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

    print("\nRFM scores calculated.")
    print("Data sample with scores:\n", df_rfm.head())

    # 定义客户分层逻辑
    avg_r = df_rfm['R_Score'].astype(float).mean()
    avg_f = df_rfm['F_Score'].astype(float).mean()
    avg_m = df_rfm['M_Score'].astype(float).mean()

    def segment_customer(row):
        is_r_high = row['R_Score'] > avg_r
        is_f_high = row['F_Score'] > avg_f
        is_m_high = row['M_Score'] > avg_m

        if is_r_high and is_f_high and is_m_high:
            return 'Champions'
        if is_f_high and is_m_high:
            return 'Loyal Customers'
        if is_r_high and is_f_high:
            return 'Potential Loyalists'
        if is_r_high:
            return 'New Customers'
        if is_f_high:
            return 'Need Attention'
        if not is_f_high and not is_m_high:
            if not is_r_high:
                return 'At Risk'
            return 'Hibernating'
        return 'About to Sleep'

    df_rfm['Segment'] = df_rfm.apply(segment_customer, axis=1)
    print("\nCustomer segmentation complete!")
    print("Final segmented data sample:\n", df_rfm.head())

    return df_rfm


def visualize_and_save(df_segmented):
    """可视化客户分层结果并保存数据"""
    plt.figure(figsize=(12, 8))

    segment_counts = df_segmented['Segment'].value_counts().sort_values(ascending=False)
    sns.barplot(x=segment_counts.index, y=segment_counts.values, palette='viridis')

    plt.title('Customer Segment Distribution', fontsize=16)
    plt.xlabel('Customer Segment', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    figure_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'figures')
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)
    plt.savefig(os.path.join(figure_path, 'customer_segmentation_distribution.png'))
    print(f"\nCustomer segmentation chart saved to: {figure_path}")
    plt.show()

    final_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'customer_segments.csv')
    df_segmented.to_csv(final_path, index=True)
    print(f"Final segmented data saved to: {final_path}")


if __name__ == "__main__":
    print("--- RFM Analysis and Segmentation Script Started ---")
    df_rfm_raw = load_rfm_data()
    df_final = calculate_scores_and_segments(df_rfm_raw)
    visualize_and_save(df_final)
    print("\n--- RFM Analysis and Segmentation Script Finished ---")