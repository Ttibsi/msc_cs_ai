import pandas
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split, cross_val_score
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, cohen_kappa_score, roc_curve

weather_data = pandas.read_csv("weather.nominal.csv", delimiter=',', encoding="utf-8")

# Features used for the decision tree
features = weather_data.iloc[:,:4]
output = weather_data.iloc[:,4]

# Turn categorical features into numeric values
features_encoded = pandas.get_dummies(features)

# Seperate into testing and training
features_train, features_test, output_train, output_test = train_test_split(
    features_encoded,
    output,
    random_state=3,
    test_size=0.5
)

# decision tree time
decision_tree = DecisionTreeClassifier(
    criterion="entropy",
    splitter="best",
    random_state=0
)

decision_tree.fit(features_train, output_train)

# display tree
#  plt.figure(figsize=(12, 6))
#  plot_tree(
#      decision_tree,
#      feature_names=features_encoded.columns,
#      class_names=decision_tree.classes_,
#      filled=True
#  )
# plt.show()

# evaluate the model
y_predict = decision_tree.predict(features_test)
confusion_m = confusion_matrix(output_test, y_predict, labels=decision_tree.classes_)
cm_display = ConfusionMatrixDisplay(
    confusion_matrix=confusion_m,
    display_labels=["no", "yes"]
)
plot = cm_display.plot()
# plt.show()

tn, fp, fn, tp = confusion_m.ravel()
y_prob = decision_tree.predict_proba(features_test)[:, 1]
precision = precision_score(output_test, y_predict, pos_label="yes")
recall = recall_score(output_test, y_predict, pos_label="yes")
f1 = f1_score(output_test, y_predict, pos_label="yes")

false_pos_rate = fp/(fp + tn)
roc_auc = roc_auc_score(output_test, y_prob)
kappa = cohen_kappa_score(output_test, y_predict)

# print(f"Precision: {precision:.2f}")
# print(f"Recall (TPR): {recall:.2f}")
# print(f"F1 Score: {f1:.2f}")
# print(f"False Positive Rate (FPR): {false_pos_rate:.2f}")
# print(f"ROC AUC Score: {roc_auc:.2f}")
# print(f"Cohen's Kappa: {kappa:.2f}")

clf = DecisionTreeClassifier(random_state = 42)
cv_scores = cross_val_score(clf, features_encoded, output, cv=4)
print("Cross-validation scores:", cv_scores)
