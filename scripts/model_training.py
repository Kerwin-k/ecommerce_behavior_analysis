# scripts/model_training.py

import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


def load_data():
    """从 processed 文件夹加载带有流失标签的数据"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'churn_data.csv')
    df = pd.read_csv(data_path)

    print("Data with churn labels loaded successfully.")
    print("Data shape:", df.shape)
    return df


def train_and_evaluate_model(df):
    """训练并评估一个流失预测模型"""

    # 1. 定义特征 (X) 和目标 (y)
    features = ['Recency', 'Frequency', 'Monetary']
    target = 'Churn'

    X = df[features]
    y = df[target]

    print(f"\nUsing Features (X): {features}")
    print(f"Predicting Target (y): {target}")

    # 2. 拆分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set size: {X_train.shape[0]} rows")
    print(f"Test set size: {X_test.shape[0]} rows")

    # 3. 初始化并训练模型
    model = LogisticRegression(random_state=42, class_weight='balanced')

    print("\nTraining Logistic Regression model...")
    model.fit(X_train, y_train)
    print("Model training complete!")

    # 4. 在测试集上进行预测和评估
    print("\nEvaluating model on the test set...")
    y_pred = model.predict(X_test)

    # 模型预测准确率（预测值pred，与实际值test对比）
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.2%}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Churned (0)', 'Churned (1)']))

    # 可视化混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Predicted: Not Churned', 'Predicted: Churned'],
                yticklabels=['Actual: Not Churned', 'Actual: Churned'])
    plt.title('Confusion Matrix')
    plt.ylabel('Actual Label')
    plt.xlabel('Predicted Label')

    figure_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'figures')
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)
    plt.savefig(os.path.join(figure_path, 'churn_confusion_matrix.png'))
    print(f"\nConfusion matrix chart saved to: {figure_path}")
    plt.show()


if __name__ == "__main__":
    print("--- Model Training Script Started ---")
    df_data = load_data()
    train_and_evaluate_model(df_data)
    print("\n--- Model Training Script Finished ---")