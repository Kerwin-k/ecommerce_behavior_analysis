import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def load_rfm_data():
    """从 processed 文件夹加载 RFM 数据"""
    rfm_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'rfm_data.csv')
    df_rfm = pd.read_csv(rfm_path)

    # 确保Invoice被正确命名为'Frequency'
    if 'Invoice' in df_rfm.columns:
        df_rfm.rename(columns={'Invoice': 'Frequency'}, inplace=True)
        print("列名 'Invoice' 已被重命名为 'Frequency'。")

    print("已成功加载 RFM 数据。")
    print("数据形状:", df_rfm.shape)
    print("数据样例:\n", df_rfm.head())
    return df_rfm


def calculate_scores_and_segments(df_rfm):
    """计算RFM分数，并根据分数进行客户分层"""
    # 1. 使用pd.qcut进行打分，它会根据数值分布自动将客户分为5个等份
    # 对于 Recency，数值越小越好，所以标签顺序是 [5, 4, 3, 2, 1]
    df_rfm['R_Score'] = pd.qcut(df_rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
    # 对于 Frequency 和 Monetary，数值越大越好，所以标签顺序是 [1, 2, 3, 4, 5]
    df_rfm['F_Score'] = pd.qcut(df_rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    df_rfm['M_Score'] = pd.qcut(df_rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

    # .rank(method='first') 用于处理F值中存在大量相同值（如都为1）导致qcut报错的问题

    print("\n已计算RFM分数。")
    print("带分数的数据样例:\n", df_rfm.head())

    # 2. 定义客户分层逻辑
    # 我们将每个得分与平均分进行比较，来划分客户
    avg_r = df_rfm['R_Score'].astype(float).mean()
    avg_f = df_rfm['F_Score'].astype(float).mean()
    avg_m = df_rfm['M_Score'].astype(float).mean()

    def segment_customer(row):
        is_r_high = row['R_Score'] > avg_r
        is_f_high = row['F_Score'] > avg_f
        is_m_high = row['M_Score'] > avg_m

        if is_r_high and is_f_high and is_m_high:
            return '高价值客户'  # Champions
        if is_f_high and is_m_high:
            return '忠诚客户'  # Loyal Customers
        if is_r_high and is_f_high:
            return '潜力客户'  # Potential Loyalists
        if is_r_high:
            return '新客户'  # New Customers
        if is_f_high:
            return '需要关注的客户'  # Need Attention
        if not is_f_high and not is_m_high:
            if not is_r_high:
                return '流失风险客户'  # At Risk
            return '休眠客户'  # Hibernating
        return '一般客户'  # About to Sleep

    df_rfm['Segment'] = df_rfm.apply(segment_customer, axis=1)
    print("\n客户分层完成！")
    print("最终分层数据样例:\n", df_rfm.head())

    return df_rfm


def visualize_and_save(df_segmented):
    """可视化客户分层结果并保存数据"""
    # 1. 可视化
    plt.figure(figsize=(12, 8))
    # 使用中文字体'SimHei'，可以换成'Microsoft YaHei'或其他支持中文的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    segment_counts = df_segmented['Segment'].value_counts().sort_values(ascending=False)

    # 修改前
    # sns.barplot(x=segment_counts.index, y=segment_counts.values, palette='viridis')

    # 修改后 (按提示)
    sns.barplot(data=segment_counts.reset_index(), x='Segment', y='count', hue='Segment', palette='viridis',
                legend=False)

    plt.title('各类客户数量分布', fontsize=16)
    plt.xlabel('客户分层', fontsize=12)
    plt.ylabel('客户数量', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()  # 调整布局防止标签重叠

    # 保存图表
    figure_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'figures')
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)
    plt.savefig(os.path.join(figure_path, 'customer_segmentation_distribution.png'))
    print(f"\n客户分层分布图已保存至: {figure_path}")
    plt.show()  # 在运行时显示图表

    # 2. 保存带分层标签的数据
    final_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'customer_segments.csv')
    df_segmented.to_csv(final_path, index=True)
    print(f"最终分层数据已保存至: {final_path}")

if __name__ == "__main__":
    print("--- RFM分析与客户分层脚本开始 ---")
    df_rfm_raw = load_rfm_data()
    df_final = calculate_scores_and_segments(df_rfm_raw)
    visualize_and_save(df_final)
    print("\n--- RFM分析与客户分层脚本运行结束 ---")