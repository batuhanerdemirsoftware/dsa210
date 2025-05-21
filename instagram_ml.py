import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, f1_score, classification_report
import joblib

def load_all_csvs(data_dir='data'):
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    dfs = []
    for f in files:
        df = pd.read_csv(os.path.join(data_dir, f))
        dfs.append(df)
    combined = pd.concat(dfs, ignore_index=True)
    return combined

def prepare_features(df):
    df = df.copy()
    df['caption_length'] = df['caption'].fillna('').apply(len)
    df['word_count'] = df['caption'].fillna('').apply(lambda x: len(str(x).split()))
    try:
        from textblob import TextBlob
        df['sentiment'] = df['caption'].fillna('').apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    except ImportError:
        df['sentiment'] = 0
    df['hashtag_count'] = df['hashtags'].fillna('').apply(lambda x: len(str(x).split(', ')) if x else 0)
    df['post_hour'] = pd.to_datetime(df['post_timestamp']).dt.hour
    post_type_dummies = pd.get_dummies(df['post_type'], prefix='type')
    X = pd.concat([
        df[['followers', 'following', 'caption_length', 'word_count', 'sentiment', 'hashtag_count', 'post_hour']],
        post_type_dummies
    ], axis=1)
    return X

def regression_task(X, y, out_dir, target_name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    results = []
    linreg = LinearRegression().fit(X_train, y_train)
    y_pred_lr = linreg.predict(X_test)
    results.append(("LinearRegression", r2_score(y_test, y_pred_lr), mean_absolute_error(y_test, y_pred_lr)))
    rf = RandomForestRegressor(random_state=42).fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    results.append(("RandomForestRegressor", r2_score(y_test, y_pred_rf), mean_absolute_error(y_test, y_pred_rf)))
    feat_imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    feat_imp.to_csv(os.path.join(out_dir, f'{target_name}_rf_feature_importances.csv'))
    with open(os.path.join(out_dir, f'{target_name}_regression_results.txt'), 'w') as f:
        for name, r2, mae in results:
            f.write(f"{name}: R2={r2:.3f}, MAE={mae:.2f}\n")
    return results

def classification_task(X, y, out_dir, target_name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    results = []
    logreg = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    y_pred_lr = logreg.predict(X_test)
    results.append(("LogisticRegression", accuracy_score(y_test, y_pred_lr), f1_score(y_test, y_pred_lr)))
    rf = RandomForestClassifier(random_state=42).fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    results.append(("RandomForestClassifier", accuracy_score(y_test, y_pred_rf), f1_score(y_test, y_pred_rf)))
    feat_imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    feat_imp.to_csv(os.path.join(out_dir, f'{target_name}_rf_feature_importances.csv'))
    with open(os.path.join(out_dir, f'{target_name}_classification_results.txt'), 'w') as f:
        for name, acc, f1 in results:
            f.write(f"{name}: Accuracy={acc:.3f}, F1={f1:.3f}\n")
        f.write("\nClassification Report (Random Forest):\n")
        f.write(classification_report(y_test, y_pred_rf))
    return results

def main():
    data_dir = 'data'
    out_dir = os.path.join('analysis_results', 'all_users')
    os.makedirs(out_dir, exist_ok=True)
    df = load_all_csvs(data_dir)
    X = prepare_features(df)
    regression_task(X, df['likes'], out_dir, 'likes')
    regression_task(X, df['comments'], out_dir, 'comments')
    y_engage = (df['likes'] > df['likes'].median()).astype(int)
    classification_task(X, y_engage, out_dir, 'high_engagement')

if __name__ == '__main__':
    main() 