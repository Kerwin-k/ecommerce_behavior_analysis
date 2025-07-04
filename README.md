# E-commerce Customer Behavior Analysis Project

## 1. Project Overview

This project aims to analyze real-world e-commerce transaction data to gain deep insights into customer behavior patterns. We utilize the **RFM model** to segment customers based on their value, identifying distinct groups such as "High-Value Customers," "At-Risk Customers," and more. The ultimate goal is to provide data-driven, actionable business recommendations to support fine-grained operations and targeted marketing strategies for the e-commerce platform.

---

## 2. Project Structure

This project uses a modular structure to ensure the code is clean, maintainable, and reproducible.
```
ecommerce_behavior_analysis/
├── data/
│   ├── raw/                # Contains the raw dataset: online_retail_II.csv
│   └── processed/          # Contains cleaned and processed data
├── reports/
│   └── figures/            # Contains visualizations generated during the analysis
├── scripts/                # Contains the core Python analysis scripts
│   ├── data_cleaning.py          # Script for data cleaning
│   ├── feature_engineering.py    # Script for feature engineering (RFM calculation)
│   └── rfm_analysis.py           # Script for RFM analysis and customer segmentation
├── .venv/                  # Python virtual environment
├── README.md               # Project documentation file
└── requirements.txt        # List of project dependencies
```
---

## 3. Technology Stack

* **Programming Language:** Python 3
* **Core Libraries:**
    * `Pandas`: For data processing and analysis.
    * `Matplotlib` & `Seaborn`: For data visualization.

---

## 4. How to Run

1.  **Clone the project locally:**
    ```bash
    git clone [Your Project's GitHub URL]
    cd ecommerce_behavior_analysis
    ```

2.  **Install dependencies:**
    It is recommended to install in a virtual environment to avoid package conflicts.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the scripts in order:**
    The entire analysis pipeline is divided into three separate scripts. Please run them in the following sequence from your terminal:

    * **Step 1: Data Cleaning**
        ```bash
        python scripts/data_cleaning.py
        ```
        This script reads the raw data from `data/raw/`, cleans it, and saves the result as `data/processed/online_retail_cleaned.csv`.

    * **Step 2: Feature Engineering (RFM Calculation)**
        ```bash
        python scripts/feature_engineering.py
        ```
        This script reads the cleaned data, calculates the R, F, and M values for each customer, and saves the result as `data/processed/rfm_data.csv`.

    * **Step 3: Customer Segmentation Analysis**
        ```bash
        python scripts/rfm_analysis.py
        ```
        This script reads the RFM data, performs scoring and segmentation, saves the final labeled data as `data/processed/customer_segments.csv`, and generates a visualization chart in the `reports/figures/` directory.

---

## 5. Analysis Process & Methodology

### 5.1 Data Cleaning
The original dataset contained over 1 million transaction records. The following cleaning steps were performed:
-   Removed ~240,000 records with missing `Customer ID`.
-   Removed records representing returns (negative `Quantity`) and items with a price of zero.
-   Converted `InvoiceDate` to a datetime format and `Customer ID` to an integer.
-   Removed ~26,000 duplicate records.
After cleaning, we obtained approximately 780,000 high-quality transaction records for further analysis.

### 5.2 RFM Model
We adopted the classic RFM model to measure customer value:
-   **R (Recency):** How recently a customer made a purchase.
-   **F (Frequency):** How often a customer made purchases within the period.
-   **M (Monetary):** How much money a customer spent within the period.

### 5.3 Customer Segmentation
Based on the calculated RFM values, we segmented customers through the following steps:
1.  **RFM Scoring:** Used `pd.qcut` to divide the customer base into five equal-sized groups (quintiles) for each metric (R, F, M) and assigned scores from 1 to 5.
2.  **Segment Definition:** Compared each customer's R/F/M scores against the average scores of the entire cohort to assign customers to one of eight segments, such as "High-Value Customers," "Loyal Customers," etc.

---

## 6. Key Findings & Insights

Visualizing the distribution of customer segments revealed the following key insights:

![Customer Segmentation Distribution](reports/figures/customer_segmentation_distribution.png)

1.  **High Churn Risk is the Primary Concern:** "At-Risk Customers" are the largest segment, indicating a significant challenge in customer retention and suggesting a relatively short customer lifecycle.
2.  **A Strong Core of High-Value Customers:** The company relies on a strong base of "High-Value Customers" to support its main revenue streams. Their loyalty is paramount.
3.  **Customer Acquisition is Healthy:** The "New Customers" segment is substantial, proving that the company can consistently attract new users, providing a foundation for growth.
4.  **A Bottleneck Exists in Customer Conversion:** The small number of "Potential Loyalists" suggests a potential weakness in converting new or infrequent customers into loyal ones.

---

## 7. Business Recommendations

| Customer Segment      | Finding                     | Recommended Marketing Strategy                                                                                                                                                                                            |
| :-------------------- | :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **At-Risk Customers** | Largest group, highest risk | **Goal:** Urgent Reactivation & Win-Back<br>**Actions:** Launch large-scale "win-back" campaigns with significant, exclusive discounts via email/SMS. Conduct surveys to understand their reasons for inactivity.                  |
| **High-Value Customers**| Core revenue source         | **Goal:** Premium Service & Value Maximization<br>**Actions:** Implement a VIP program with exclusive benefits like dedicated support, early access to new products, and birthday gifts. Promote high-margin products or bundles. |
| **New Customers** | Hope for future growth      | **Goal:** Increase First-Purchase Retention<br>**Actions:** Optimize the post-purchase experience with a "welcome email series." Offer a small, exclusive discount for their second purchase to encourage repeat business.    |
| **Potential Loyalists** | Low quantity, poor conversion| **Goal:** Nurture & Incentivize<br>**Actions:** Treat this group as a key operational focus. Analyze their preferences to provide targeted product recommendations and marketing campaigns to increase their purchase frequency. |

---

## 8. Conclusion & Future Work

This project successfully segmented an e-commerce customer base using the RFM model, uncovering key insights into the customer structure, challenges, and opportunities. The proposed business recommendations are designed to help the company achieve fine-grained customer operations to improve retention and overall profitability.

**Future work could explore:**
-   **Churn Prediction Model:** Build a machine learning model (e.g., Logistic Regression, Random Forest) to predict the probability of a customer churning.
-   **Basket Analysis:** Use association rule algorithms like Apriori to discover which products are frequently bought together.
-   **Customer Lifetime Value (CLV) Prediction:** Develop more complex models to forecast the total revenue a customer will generate throughout their entire relationship with the company.

---

## 9. Team Members