import pandas as pd
import shap

url = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"

df = pd.read_csv(url)

print(df.head())

print(df["Class"].value_counts(normalize=True))

import numpy as np
df["Amount_log"] = np.log1p(df["Amount"])

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df["Amount_scaled"] = scaler.fit_transform(df[["Amount"]])

from sklearn.model_selection import train_test_split
x = df.drop("Class", axis=1)
y = df["Class"]
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

from sklearn.metrics import classification_report
report = classification_report(y_test, y_pred)
print(report)

from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

y_prob = model.predict_proba(x_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_prob)

plt.plot(fpr, tpr)
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.title('Curva ROC')
plt.show()
print(f'AUC: {roc_auc_score(y_test, y_prob):.2f}')

from sklearn.metrics import precision_recall_curve

precision, recall, _ = precision_recall_curve(y_test, y_prob)
plt.plot(recall, precision)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Curva Precision-Recall')
plt.show()

#Undersampling
fraudes = df[df["Class"] == 1]
normais = df[df["Class"] == 0].sample(len(fraudes), random_state=42)
df_under = pd.concat([fraudes, normais])
print(df_under["Class"].value_counts())

#Oversampling
from imblearn.over_sampling import SMOTE
smote = SMOTE()
x_over, y_over = smote.fit_resample(x, y)
print(pd.Series(y_over).value_counts())

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(
    n_estimators=50,
    max_depth=10,
    class_weight='balanced',
    n_jobs=-1,
    random_state=42
)
rf.fit(x_train, y_train)
y_pred_rf = rf.predict(x_test)
print(classification_report(y_test, y_pred_rf))

from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=1000))
])

pipeline.fit(x_train, y_train)
y_pred_pipeline = pipeline.predict(x_test)

threshold = 0.3
y_pred_custom = (y_prob > threshold).astype(int)
print(classification_report(y_test, y_pred_custom))

from xgboost import XGBClassifier
xgb = XGBClassifier(
    scale_pos_weight=10,
    use_label_encoder=False,
    eval_metric='logloss'
)
xgb.fit(x_train, y_train)
y_pred_xgb = xgb.predict(x_test)

print(classification_report(y_test, y_pred_xgb))

importancias = xgb.feature_importances_
plt.bar(range(len(importancias)), importancias)
plt.title('Importância das Variáveis')
plt.show()

from sklearn.model_selection import GridSearchCV
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [3, 5]
}
grid = GridSearchCV(
    XGBClassifier(eval_metric='logloss'),
    param_grid,
    scoring='recall',
    cv=3,
)
grid.fit(x_train, y_train)
print(f'Melhor modelo: {grid.best_params_}')

explainer = shap.TreeExplainer(xgb)
shap_values = explainer(x_test[:100])

shap.plots.bar(shap_values)
