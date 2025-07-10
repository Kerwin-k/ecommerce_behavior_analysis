[Read this in Chinese (阅读中文版)](README_zh-CN.md)

---
# E-commerce Customer Behavior Analysis Project

## 1. Project Overview

This project provides a comprehensive end-to-end analysis of an e-commerce transaction dataset. The primary objectives are to understand customer behavior, segment customers based on their value, and build a predictive model for customer churn. Key methodologies include the **RFM model** for customer segmentation and a **Logistic Regression model** for churn prediction. The final output delivers actionable, data-driven insights to support targeted marketing and customer retention strategies.

## 2. Project Structure

This project uses a modular structure to ensure the code is clean, maintainable, and reproducible.

```
ecommerce_behavior_analysis/
├── data/
│   ├── raw/                # Contains the raw dataset: online_retail_II.csv
│   └── processed/          # Contains cleaned and processed data files
├── reports/
│   └── figures/            # Contains visualizations generated during the analysis
├── scripts/                # Contains the core Python analysis scripts
│   ├── data_cleaning.py          # Script for data cleaning
│   ├── feature_engineering.py    # Script for feature engineering (RFM calculation)
│   ├── rfm_analysis.py           # Script for RFM analysis and customer segmentation
│   ├── churn_label.py            # Script to label customers as churned/active
│   ├── model_training.py         # Script to train and evaluate the churn prediction model
│   └── visualization.py          # Script to generate a dashboard of key visualizations
├── .venv/                  # Python virtual environment
├── README.md               # This documentation file
└── requirements.txt        # List of project dependencies
```

## 3. Technology Stack

* **Programming Language:** Python 3
* **Core Libraries:**
    * `Pandas`: For data processing and analysis.
    * `Scikit-learn`: For machine learning (modeling and evaluation).
    * `Matplotlib` & `Seaborn`: For data visualization.

## 4. How to Run

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Kerwin-k/ecommerce_behavior_analysis.git
    cd ecommerce_behavior_analysis
    ```

2.  **Install Dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Scripts in Order:**
    The entire analysis pipeline must be run in the following sequence:

    ```bash
    # 1. Clean the raw data
    python scripts/data_cleaning.py

    # 2. Calculate RFM metrics
    python scripts/feature_engineering.py

    # 3. Score and segment customers based on RFM
    python scripts/rfm_analysis.py

    # 4. Label customers for the churn model
    python scripts/churn_label.py

    # 5. Train and evaluate the churn prediction model
    python scripts/model_training.py

    # 6. Generate all summary visualizations
    python scripts/visualization.py
    ```
    
## 5. Analysis Process & Methodology

### 5.1 Data Cleaning
The original dataset was cleaned by removing records with missing `Customer ID`, handling returns (negative `Quantity`), removing zero-price items, and dropping duplicate entries. This process refined the dataset from over 1 million rows to approximately 780,000 high-quality transaction records.

### 5.2 Customer Segmentation (RFM Model)
We used the RFM model to quantify customer value based on:
-   **R (Recency):** How recently a customer made a purchase.
-   **F (Frequency):** How often they make purchases.
-   **M (Monetary):** How much money they spend.
Customers were scored on each dimension and then grouped into 8 distinct segments, such as 'Champions', 'At Risk', etc.

### 5.3 Predictive Modeling (Customer Churn Prediction)
To predict customer churn, we developed a machine learning model:
-   **Label Definition:** Customers in the 'At Risk' and 'Hibernating' segments were labeled as "Churned" (1), while all others were labeled as "Active" (0).
-   **Feature Selection:** The calculated `Recency`, `Frequency`, and `Monetary` values were used as the input features for the model.
-   **Model & Evaluation:** A Logistic Regression model was trained on 80% of the data. On the remaining 20% test set, the model achieved an **accuracy of ~90%** and, more importantly, a **recall of 90%** for the churned class, successfully identifying 9 out of 10 customers who were at risk of churning.

## 6. Key Findings & Insights

### Customer Segmentation
The distribution of customer segments reveals the health of the customer base. The largest group consists of "At-Risk Customers," highlighting a significant challenge in customer retention. However, a strong core of "Champions" (High-Value) and "Loyal Customers" forms the backbone of the business.

![Customer Segmentation Distribution](reports/figures/customer_segmentation_distribution.png)

### Churn Prediction Model Performance
The confusion matrix visually confirms the model's high performance, particularly its ability to correctly identify customers who are likely to churn.

![Churn Prediction Confusion Matrix](reports/figures/churn_confusion_matrix.png)

### Additional Insights
-   **RFM Distributions:** The histograms show that most customers have high Recency (have not purchased recently) and low Frequency, which is typical for many retail businesses.
-   **Sales Trends:** The monthly sales trend chart indicates seasonality in sales, which can inform inventory and marketing planning.
-   **Geographical Distribution:** The analysis of top countries by sales (excluding the UK) helps identify key secondary markets for potential growth.

![RFM Distributions](reports/figures/rfm_distributions.png)
![Monthly Sales Trend](reports/figures/monthly_sales_trend.png)

## 7. Business Recommendations

| Customer Segment      | Finding                     | Recommended Marketing Strategy                                                                                                                                                                                            |
| :-------------------- | :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **At-Risk Customers** | Largest group, highest risk | **Goal:** Urgent Reactivation & Win-Back<br>**Actions:** Use the predictive model to identify these users proactively. Launch "win-back" campaigns with significant, personalized discounts. Survey them to understand reasons for inactivity. |
| **Champions** | Core revenue source         | **Goal:** Premium Service & Reward<br>**Actions:** Implement a VIP program with exclusive benefits like early access to new products and dedicated support. Encourage them to become brand advocates.                           |
| **New Customers** | Hope for future growth      | **Goal:** Increase First-Purchase Retention<br>**Actions:** Optimize the post-purchase experience with a "welcome email series." Offer a small, exclusive discount for their second purchase to encourage repeat business.    |
| **Potential Loyalists**| Low quantity, poor conversion| **Goal:** Nurture & Incentivize<br>**Actions:** Treat this group as a key operational focus. Analyze their preferences to provide targeted product recommendations and marketing campaigns to increase their purchase frequency. |

## 8. Conclusion & Future Work

This project successfully demonstrates an end-to-end data analysis pipeline, from data cleaning to descriptive analytics (RFM) and predictive analytics (churn model). The findings provide a clear view of the customer landscape and offer concrete, data-driven strategies to enhance customer retention and drive growth.

**Future work could explore:**
-   **Improving the Churn Model:** Engineer more features (e.g., product diversity, time between purchases) and experiment with more advanced models like XGBoost to further improve predictive accuracy.
-   **Basket Analysis:** Use association rule mining to discover which products are frequently bought together.
-   **Customer Lifetime Value (CLV) Prediction:** Forecast the total revenue a customer will generate throughout their entire relationship with the company.

## 9. Team Members

* Liu Kun, Li Dan
* MDT1007 Project