# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k1yqgxHUhScnLhdMLRQIyN23d2nakGC1
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_curve, f1_score, roc_auc_score, precision_score,recall_score,roc_curve, auc
from sklearn.model_selection import train_test_split
from scipy.stats import chi2_contingency
from matplotlib import rcParams
from matplotlib import rcParams
import warnings

def read_csv(filename):
    "Read the csv file into a dataframe"
    try:
        return pd.read_csv(filename)
    except Exception as e:
        print("Error:", str(e))
        return None

def drop_null_values(df):
    """Drop rows with null values"""
    if df is not None:
        df.dropna(inplace=True)
    else:
        print("Error: DataFrame is None")

def drop_duplicates(df):
    """Drop duplicate rows from the DataFrame."""
    if df is not None:
        df.drop_duplicates(inplace=True)
    else:
        print("Error: DataFrame is None")

def rename_columns(df):
    """Rename columns"""
    if df is not None:
        df.rename(columns={'PhysicalHealthDays': 'BadPhysicalHealthDays', 'MentalHealthDays': 'BadMentalHealthDays'}, inplace=True)
    else:
        print("Error: DataFrame is None")

def encode_categorical_features(df):
    """Encode categorical features"""
    if df is not None:
        le = LabelEncoder()
        categorical_features = df.select_dtypes(["object", "category", "bool"]).columns.tolist()
        for label in categorical_features:
            if len(df[label].unique()) <= 2:
                df[label] = le.fit_transform(df[label])
            else:
                df = pd.get_dummies(df, columns=[label])
        return df
    else:
        print("Error: DataFrame is None")
        return None

def preprocess_data(df):
    "Preprocess data"
    drop_null_values(df)
    drop_duplicates(df)
    rename_columns(df)

def calculate_cramers_v(x, y):
    """Calculate Cramér's V for each feature selection"""
    cramers_v_values = {}
    for column in x.columns:
        cramers_v_values[column] = cramers_v(x[column], y)
    return cramers_v_values

def cramers_v(x, y):
    """Calculate Cramér's V for two categorical variables."""
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

def drop_columns(df):
    """Drop specified columns from the DataFrame."""
    columns_to_drop = ['HadAsthma', 'HadSkinCancer',
                       'HadDepressiveDisorder',
                       'HeightInMeters', 'WeightInKilograms',
                       'HIVTesting', 'FluVaxLast12', 'TetanusLast10Tdap',
                       'HighRiskLastYear', 'CovidPos',
                       'ECigaretteUsage_Never used e-cigarettes in my entire life',
                       'ECigaretteUsage_Not at all (right now)',
                       'ECigaretteUsage_Use them every day',
                       'ECigaretteUsage_Use them some days',
                       'RaceEthnicityCategory_Black only, Non-Hispanic',
                       'RaceEthnicityCategory_Hispanic',
                       'RaceEthnicityCategory_Multiracial, Non-Hispanic',
                       'RaceEthnicityCategory_Other race only, Non-Hispanic',
                       'RaceEthnicityCategory_White only, Non-Hispanic']

    df.drop(columns=columns_to_drop, inplace=True)

    # Ensure at least one column remains in the DataFrame
    if len(df.columns) == 0:
        raise ValueError("Cannot drop all columns, at least one column must remain.")

def under_sample(df, target, threshold_percentage, random_state=42):
    """Undersample the majority class to balance the dataset."""
    minority_class_len = len(df[df[target] == 1])
    undersampling_count = int(minority_class_len * threshold_percentage)
    majority_class_indices = df[df[target] == 0].index
    random_majority_indices = np.random.choice(majority_class_indices, undersampling_count, replace=False)
    under_sample_indices = np.concatenate([df[df[target] == 1].index, random_majority_indices])
    under_sample = df.loc[under_sample_indices]
    return under_sample

def logistic_regression_model(x_train, x_test, y_train, y_test, threshold=0.3):
    '''Fit logistic regression model'''
    model = LogisticRegression()
    model.fit(x_train, y_train)

    '''Predict probabilities and then threshold the probabilities to get binary predictions'''
    y_pred_prob = model.predict_proba(x_test)[:, 1]  # Probabilities of positive class
    y_pred = (y_pred_prob > threshold).astype(int)

    return model, y_pred, y_pred_prob  # Return trained model and predictions

def save_model_with_preprocessing(model, filename):

    with open(filename, 'wb') as f:
        pickle.dump((model), f)

def evaluate_model(y_test, y_pred, y_pred_prob):
    """Evaluate the logistic regression model"""
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)
    precision, recall, _ = precision_recall_curve(y_test, y_pred_prob)
    f1 = f1_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_prob)

    return accuracy, conf_matrix, class_report, precision, recall, f1, auc_score


def main():
    df = read_csv("heartDisease.csv")

    '''Preprocess the data'''
    rename_columns(df)
    df = encode_categorical_features(df)

    x = df.drop(columns=['HadHeartAttack'])
    y = df['HadHeartAttack']
    cramers_v_values = calculate_cramers_v(x, y)

    sorted_cramers_v_values = dict(sorted(cramers_v_values.items(), key=lambda item: item[1], reverse=True))

    for feature, v in sorted_cramers_v_values.items():
        print(f"Cramér's V for {feature}: {v}")

    drop_columns(df)
    target = 'HadHeartAttack'

#     %matplotlib inline
    rcParams['figure.figsize'] = 10, 6
    warnings.filterwarnings('ignore')
    sns.set(style="darkgrid")

    # Undersampling
    print(df[target].value_counts())

    threshold_percentage = 2

    under_sampled_df = under_sample(df, target, threshold_percentage)
    print(under_sampled_df[target].value_counts())
    x = under_sampled_df.loc[:, df.columns != target]
    y = under_sampled_df.loc[:, df.columns == target]

    '''Split data into training and testing sets'''
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    '''Train the logistic regression model and get predictions'''
    model, y_pred, y_pred_prob = logistic_regression_model(x_train, x_test, y_train, y_test)

    '''Evaluate the model'''
    accuracy, conf_matrix, class_report, precision, recall, f1, auc_score = evaluate_model(y_test, y_pred, y_pred_prob)
    print("Accuracy:", accuracy)
    print("Confusion Matrix:\n", conf_matrix)
    print("Classification Report:\n", class_report)
    print("F1 Score:", f1)
    print("AUC Score:", auc_score)

    '''testing'''
    test_data = read_csv("Heartdisease1.csv")
    rename_columns(test_data)
    test_data = encode_categorical_features(test_data)

    df_predict = test_data.drop(columns=['HadHeartAttack'])

    '''Make predictions on the new data'''
    new_predictions = model.predict(df_predict)
    prediction_scores = model.predict_proba(df_predict)
    print(df_predict.iloc[0])

    '''Print the actual and predicted values'''
    result_df = pd.DataFrame({'Actual': test_data['HadHeartAttack'], 'Predicted': new_predictions})

    '''Compute accuracy score'''
    accuracy = accuracy_score(test_data['HadHeartAttack'], new_predictions)
    print("Accuracy:", accuracy)

    '''Print the result dataframe'''
    print(result_df)
    print(prediction_scores)

    save_model_with_preprocessing(model, 'heart_disease_model.pkl')

if __name__ == "__main__":
    main()

