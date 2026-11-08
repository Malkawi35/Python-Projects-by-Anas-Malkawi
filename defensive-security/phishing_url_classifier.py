
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: [This fetches the dataset from the CSV file from the path]
df = pd.read_csv(r"[place dataset filepath here from https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset") #Download the dataset and put where your python file is located in the c drive.
# This will help reinforce clarity
df['label'] = df['label'] #setting the label from the end of the dataset: 0 = phishing, 1 = legitimate

# Step 2: [This extract features from urls such as the length of the url, or hyphens as the output shows]
def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path + parsed.query
    return {
        'url_length': len(url),
        'num_dots': domain.count('.'),
        'has_hyphen': int('-' in domain),
        'has_at_symbol': int('@' in url),
        'has_ip_address': int(bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain))),
        'num_special_chars': sum(url.count(c) for c in ['?', '=', '&']),
        'has_suspicious_keywords': int(any(k in url.lower() for k in ['login', 'verify', 'account', 'secure', 'update']))
    }

# Step 3: [This code applies and the feature extraction function to the url and converts the results to a dataframe]
features_df = df['URL'].apply(extract_features).apply(pd.Series)

# Step 4: [This seperates the data into features which is x and target the labels for the model training which y]
X = features_df
y = df['label']

# Step 5: [This splits the data into training and testing]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# Step 6: [This trains a random forest classifier on training data]
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Step 7: [In this code it will predict the test data and display performance metrics]
y_pred = clf.predict(X_test)
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))
print("=== Confusion Matrix ===")
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Legit', 'Phish'], yticklabels=['Legit', 'Phish'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Step 8: [This displays the feature importance scores to identify most useful features]
importances = clf.feature_importances_
feat_series = pd.Series(importances, index=X.columns).sort_values(ascending=False)
print("=== Feature Importances ===")
print(feat_series)
feat_series.plot(kind='bar', title="Feature Importance", figsize=(8, 4))
plt.ylabel("Importance Score")
plt.tight_layout()
plt.show()
