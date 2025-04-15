import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import os
import zipfile
import numpy as np
# Load datasets
user_profile = pd.read_csv('user_profile.csv')
behavior_log = pd.read_csv('behavior_log.csv')
ad_feature = pd.read_csv('ad_feature.csv')
raw_sample = pd.read_csv('raw_sample.csv')

# Merge datasets
merged_data = raw_sample.merge(user_profile, left_on='user', right_on='userid')
merged_data = merged_data.merge(ad_feature, on='adgroup_id')
merged_data = merged_data.merge(behavior_log, on='user', suffixes=('_ad', '_behavior'))

# Drop unnecessary columns
merged_data.drop(columns=['userid', 'user', 'adgroup_id'], inplace=True)

# Handle missing values if any
merged_data.fillna(method='ffill', inplace=True)
print(merged_data.columns)
# Convert categorical variables into numerical values (e.g., one-hot encoding)
merged_data = pd.get_dummies(merged_data, columns=['final_gender_code', 'age_level', 'pvalue_level', 'shopping_level', 'occupation', 'new_user_class_level'])

# Split data into features and target
X = merged_data.drop(columns=['clk'])
y = merged_data['clk']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features

scaler = StandardScaler()
X_train = X_train.select_dtypes(include=[np.number])
X_test = X_test.select_dtypes(include=[np.number])
# X_train_encoded = pd.get_dummies(X_train, drop_first=True)
# X_test_encoded = pd.get_dummies(X_test, drop_first=True)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create the directory for processed data
# os.makedirs('processed_data', exist_ok=True)
# X_train_encoded = pd.get_dummies(X_train, drop_first=True)


# Export processed datasets to the new directory
merged_data.to_csv('processed_data/merged_data.csv', index=False)
# X_train_df = pd.DataFrame(X_train, columns=X_train_encoded.columns)
# X_train_df.to_csv('processed_data/X_train.csv', index=False)
# X_test_df = pd.DataFrame(X_test, columns=X_test_encoded.columns)
# X_test_df.to_csv('processed_data/X_test.csv', index=False)
# y_train.to_csv('processed_data/y_train.csv', index=False)
# Export processed datasets to the new directory
# merged_data.to_csv('processed_data/merged_data.csv', index=False)
X_train_df = pd.DataFrame(X_train, columns=X.columns)
X_train_df.to_csv('processed_data/X_train.csv', index=False)
X_test_df = pd.DataFrame(X_test, columns=X.columns)
X_test_df.to_csv('processed_data/X_test.csv', index=False)
y_train.to_csv('processed_data/y_train.csv', index=False)
y_test.to_csv('processed_data/y_test.csv', index=False)

# Create a zip file containing all the exported data
with zipfile.ZipFile('processed_data.zip', 'w') as zipf:
    zipf.write('processed_data/merged_data.csv', arcname='merged_data.csv')
    zipf.write('processed_data/X_train.csv', arcname='X_train.csv')
    zipf.write('processed_data/X_test.csv', arcname='X_test.csv')
    zipf.write('processed_data/y_train.csv', arcname='y_train.csv')
    zipf.write('processed_data/y_test.csv', arcname='y_test.csv')

# Train and evaluate KNN model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
knn_predictions = knn.predict(X_test)
print("KNN Model Performance:")
print(classification_report(y_test, knn_predictions))

# Train and evaluate Decision Tree model
decision_tree = DecisionTreeClassifier(random_state=42)
decision_tree.fit(X_train, y_train)
dt_predictions = decision_tree.predict(X_test)
print("Decision Tree Model Performance:")
print(classification_report(y_test, dt_predictions))

# Train and evaluate SVM model
svm = SVC(random_state=42)
svm.fit(X_train, y_train)
svm_predictions = svm.predict(X_test)
print("SVM Model Performance:")
print(classification_report(y_test, svm_predictions))