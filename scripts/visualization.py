# scripts/visualization.py

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(file_name):
    """一个通用的数据加载函数"""
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', file_name)
    if not os.path.exists(path):
        print(f"Error: Data file not found at {path}")
        return None

    # 针对不同文件，做一些特别处理
    if 'cleaned' in file_name:
        df = pd.read_csv(path, parse_dates=['InvoiceDate'])
    else:
        df = pd.read_csv(path)

    print(f"Successfully loaded {file_name}")
    return df


def plot_rfm_distributions(df_rfm, output_path):
    """绘制 R, F, M 三个指标的分布直方图"""
    print("Generating RFM distributions plot...")
    plt.figure(figsize=(18, 5))

    # Recency 分布
    plt.subplot(1, 3, 1)
    sns.histplot(df_rfm['Recency'], kde=True, bins=30)
    plt.title('Recency Distribution')

    # Frequency 分布 (由于F值高度偏斜，我们只看一个范围)
    plt.subplot(1, 3, 2)
    sns.histplot(df_rfm['Frequency'].loc[df_rfm['Frequency'] < 50], kde=False, bins=30)
    plt.title('Frequency Distribution (F < 50)')

    # Monetary 分布 (M值也可能偏斜，取对数或筛选范围可以看得更清)
    plt.subplot(1, 3, 3)
    sns.histplot(df_rfm['Monetary'].loc[df_rfm['Monetary'] < 10000], kde=False, bins=50)
    plt.title('Monetary Distribution (M < 10000)')

    plt.suptitle('RFM Distributions', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_path)
    plt.show()
    print(f"RFM distributions plot saved to {output_path}")


def plot_segment_scatter(df_segments, output_path):
    """绘制客户分层的散点图 (Recency vs Frequency)"""
    print("Generating segment scatter plot...")
    plt.figure(figsize=(12, 8))

    sns.scatterplot(data=df_segments, x='Recency', y='Frequency', hue='Segment', alpha=0.7, s=50)

    plt.title('Customer Segments (Recency vs Frequency)')
    plt.xlabel('Recency (Days)')
    plt.ylabel('Frequency')
    plt.legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()
    print(f"Segment scatter plot saved to {output_path}")


def plot_monthly_sales(df_cleaned, output_path):
    """绘制月度销售总额趋势图"""
    print("Generating monthly sales trend plot...")
    # 重新计算TotalPrice，因为之前的脚本没有保存它
    df_cleaned['TotalPrice'] = df_cleaned['Quantity'] * df_cleaned['Price']

    # 将InvoiceDate设置为索引，方便按时间重采样
    df_time = df_cleaned.set_index('InvoiceDate')

    # 'M' 表示按月(Month End)重采样，并计算每个月的总销售额
    monthly_sales = df_time['TotalPrice'].resample('M').sum()

    plt.figure(figsize=(15, 7))
    monthly_sales.plot(kind='line', marker='o')

    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()
    print(f"Monthly sales trend plot saved to {output_path}")


def plot_top_countries(df_cleaned, output_path):
    """绘制 Top 10 销售额国家的条形图"""
    print("Generating top 10 countries by sales plot...")
    # 确保TotalPrice存在
    if 'TotalPrice' not in df_cleaned.columns:
        df_cleaned['TotalPrice'] = df_cleaned['Quantity'] * df_cleaned['Price']

    # 按国家分组，计算销售总额，并排序
    country_sales = df_cleaned.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False)

    # 排除英国，因为它占比过大，会影响其他国家的可视化效果
    top_10_countries = country_sales.drop('United Kingdom').head(10)

    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_10_countries.values, y=top_10_countries.index, palette='mako')

    plt.title('Top 10 Countries by Sales (Excluding UK)')
    plt.xlabel('Total Sales')
    plt.ylabel('Country')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()
    print(f"Top 10 countries plot saved to {output_path}")


if __name__ == "__main__":
    print("--- Visualization Script Started ---")

    # 定义输出目录
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'reports', 'figures')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 加载所需数据
    df_rfm = load_data('rfm_data.csv')
    df_segments = load_data('customer_segments.csv')
    df_cleaned = load_data('online_retail_cleaned.csv')

    # 检查数据是否加载成功
    if df_rfm is not None:
        plot_rfm_distributions(df_rfm, os.path.join(output_dir, 'rfm_distributions.png'))

    if df_segments is not None:
        plot_segment_scatter(df_segments, os.path.join(output_dir, 'segment_scatter_plot.png'))

    if df_cleaned is not None:
        plot_monthly_sales(df_cleaned, os.path.join(output_dir, 'monthly_sales_trend.png'))
        plot_top_countries(df_cleaned, os.path.join(output_dir, 'top_10_countries.png'))

    print("\n--- Visualization Script Finished ---")