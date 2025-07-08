[Read this in English](README.md)

---
# 电商客户行为分析项目

## 1. 项目概述

本项目对一个真实的电商交易数据集进行了全面的端到端分析。项目的主要目标是理解客户行为、利用RFM模型进行客户价值分层，并构建一个预测客户流失的机器学习模型。核心分析方法包括用于客户细分的**RFM模型**和用于流失预测的**逻辑回归模型**。项目最终产出数据驱动的、可执行的洞察，以支持精细化营销和客户挽留策略。

## 2. 项目结构

本项目采用模块化的结构，确保代码的清晰、可维护和可复现。

```plaintext
ecommerce_behavior_analysis/
├── data/
│   ├── raw/                # 存放原始数据集 online_retail_II.csv
│   └── processed/          # 存放清洗和处理后的数据文件
├── reports/
│   └── figures/            # 存放分析过程中生成的可视化图表
├── scripts/                # 存放核心的Python分析脚本
│   ├── data_cleaning.py          # 数据清洗脚本
│   ├── feature_engineering.py    # 特征工程脚本 (计算RFM)
│   ├── rfm_analysis.py           # RFM分析与客户分层脚本
│   ├── churn_label.py            # 为客户打流失标签的脚本
│   ├── model_training.py         # 训练和评估流失预测模型的脚本
│   └── visualization.py          # 生成所有核心可视化图表的脚本
├── .venv/                  # Python虚拟环境
├── README.md               # 本项目说明文件
└── requirements.txt        # 项目依赖库列表
```

## 3. 技术栈

* **编程语言:** Python 3
* **核心库:**
    * `Pandas`: 用于数据处理和分析
    * `Scikit-learn`: 用于机器学习（建模与评估）
    * `Matplotlib` & `Seaborn`: 用于数据可视化

## 4. 如何运行

1.  **克隆项目到本地:**
    ```bash
    git clone [你的项目GitHub链接]
    cd ecommerce_behavior_analysis
    ```

2.  **安装依赖:**
    建议在虚拟环境中安装，以避免包版本冲突。
    ```bash
    pip install -r requirements.txt
    ```

3.  **按顺序执行脚本:**
    整个分析流程必须按以下顺序在终端中运行：

    ```bash
    # 1. 清洗原始数据
    python scripts/data_cleaning.py

    # 2. 计算RFM指标
    python scripts/feature_engineering.py

    # 3. 基于RFM进行打分和客户分层
    python scripts/rfm_analysis.py

    # 4. 为流失模型准备标签
    python scripts/churn_label.py

    # 5. 训练并评估流失预测模型
    python scripts/model_training.py

    # 6. 生成所有汇总的可视化图表
    python scripts/visualization.py
    ```
    
## 4. 如何运行

1.  **克隆项目到本地:**
    ```bash
    git clone [你的项目GitHub链接]
    cd ecommerce_behavior_analysis
    ```

2.  **安装依赖:**
    建议在虚拟环境中安装，以避免包版本冲突。
    ```bash
    pip install -r requirements.txt
    ```

3.  **按顺序执行脚本:**
    整个分析流程必须按以下顺序在终端中运行：

    ```bash
    # 1. 清洗原始数据
    python scripts/data_cleaning.py

    # 2. 计算RFM指标
    python scripts/feature_engineering.py

    # 3. 基于RFM进行打分和客户分层
    python scripts/rfm_analysis.py

    # 4. 为流失模型准备标签
    python scripts/churn_label.py

    # 5. 训练并评估流失预测模型
    python scripts/model_training.py

    # 6. 生成所有汇总的可视化图表
    python scripts/visualization.py
    ```
    
## 5. 分析流程与方法

### 5.1 数据清洗
原始数据集经过清洗，移除了缺失`Customer ID`的记录、处理了退货和价格为零的条目，并删除了重复数据。数据量从超过100万条精简至约78万条高质量交易记录。

### 5.2 客户分层 (RFM模型)
我们使用RFM模型量化客户价值：
-   **R (Recency):** 最近一次消费时间
-   **F (Frequency):** 消费频率
-   **M (Monetary):** 消费金额
通过对每个维度进行打分，我们将客户划分为8个不同的群体，如“高价值客户”、“流失风险客户”等。

### 5.3 预测性建模 (客户流失预测)
我们构建了一个机器学习模型来预测客户流失：
-   **标签定义:** 将“流失风险客户”和“休眠客户”定义为“已流失”(1)，其余为“活跃”(0)。
-   **特征选择:** 使用计算出的 `Recency`, `Frequency`, `Monetary` 值作为模型的输入特征。
-   **模型与评估:** 使用逻辑回归模型在80%的数据上进行训练。在20%的测试集上，模型达到了**约90%的准确率**，以及对于流失客户**高达90%的召回率**，这意味着它成功识别了10个流失客户中的9个。

## 6. 核心发现与洞察

### 客户分层
客户群体的分布揭示了客户群的健康状况。最大的群体是“流失风险客户”，凸显了客户留存方面的巨大挑战。然而，一个由“高价值客户”和“忠诚客户”组成的强大核心是业务的支柱。

![客户分层数量分布](reports/figures/customer_segmentation_distribution.png)

### 流失预测模型表现
混淆矩阵直观地证实了模型的高性能，特别是其准确识别潜在流失客户的能力。

![流失预测混淆矩阵](reports/figures/churn_confusion_matrix.png)

### 其他洞察
-   **RFM分布:** 直方图显示，大多数客户的Recency值较高（近期未购买）、Frequency值较低，这是许多零售业务的典型特征。
-   **销售趋势:** 月度销售趋势图揭示了销售的季节性，可为库存和营销规划提供信息。
-   **地理分布:** 对Top 10销售国家的分析有助于识别有增长潜力的关键次级市场。

![RFM分布图](reports/figures/rfm_distributions.png)
![月度销售趋势图](reports/figures/monthly_sales_trend.png)

## 7. 商业建议

| 客户群体 | 发现 | 营销策略建议 |
| :--- | :--- | :--- |
| **流失风险客户** | 数量最多，风险最高 | **目标：** 紧急唤醒与召回<br>**措施：** 使用预测模型主动识别这些用户。发起“老用户召回”活动，提供大额专属折扣。调研他们不活跃的原因。 |
| **高价值客户** | 核心收入来源 | **目标：** 提供高级服务与奖励<br>**措施：** 建立VIP计划，提供新品优先体验、专属客服等特权。鼓励他们成为品牌宣传者。 |
| **新客户** | 未来增长的希望 | **目标：** 提升首次复购率<br>**措施：** 优化购后体验，设计“欢迎邮件系列”。为他们的第二次购买提供小额折扣以鼓励复购。 |
| **潜力客户**| 数量过少，转化不足 | **目标：** 重点培育与激励<br>**措施：** 将该群体作为重点运营对象，分析其偏好，进行精准的商品推荐和营销活动，以提高其购买频率。 |

## 8. 总结与未来展望

本项目成功演示了一个端到端的数据分析流程，从数据清洗到描述性分析(RFM)和预测性分析(流失模型)。分析结果清晰地描绘了客户画像，并为提升客户留存率和驱动业务增长提供了具体的、数据驱动的策略。

**未来可探索的方向：**
-   **优化流失预测模型：** 构建更多特征（如购买周期、商品多样性等），并尝试XGBoost等更高级的模型来进一步提升预测精度。
-   **购物篮分析：** 使用关联规则算法（如Apriori）来发现哪些商品经常被一起购买。
-   **客户生命周期价值(CLV)预测：** 建立更复杂的模型来预测每个客户在未来能带来的总价值。

## 9. 团队成员

* Liu Kun, Li Dan
* MDT1007 Project