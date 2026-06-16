# Logistic regression model

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

df = pd.read_csv('diabetes.csv')
# print(df.value_counts())

x = df.iloc[:, :-1]
y = df["class"]

X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=0
)

model = LogisticRegression(max_iter=1000, random_state=0)
model.fit(X_train, y_train)
# print(model.coef_)

preds = model.predict(X_test)
report = classification_report(y_test, preds)
print(report)

conf_matrix = pd.DataFrame(
    confusion_matrix(y_test, preds),
    index=["Actual: tested_negative", "Actual: tested_positive"],
    columns=["Predicted: tested_negative", "Predicted: tested_positive"]
)
print(conf_matrix)

