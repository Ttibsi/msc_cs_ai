from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the dataset
data = load_iris()

# The data containing the features used the classification is in the field 'data'
# The training and testing sets are the same as we use the full data set for training
X_train = X_test = data.data

# The data containing the classified instances is in the field target
# Again, the training and testing sets are the same as we use the full data set for training
y_train = y_test= data.target

# Train a Decision Tree
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Make predictions and evaluate
y_pred = clf.predict(X_test)
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report for Full training set:\n",
classification_report(y_test, y_pred, target_names=data.target_names))

# Naive Bayes Model
modelNB = GaussianNB()
modelNB.fit(X_train, y_train)

# Predict on the test set
y_pred = modelNB.predict(X_test)

# Evaluation
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report for Naive Bayes Model:\n",
classification_report(y_test, y_pred, target_names=data.target_names))

# Support Vector Model
# Feature scaling (recommended for SVM)
feature_scaler = StandardScaler()
X_train_scaled = feature_scaler.fit_transform(X_train)

# Create and train an SVM classifier using SMO (implicitly)
model = SVC(kernel='linear') # or 'rbf', 'poly' depending on your preference
model.fit(X_train_scaled, y_train)

# Predict on the test set, which needs to be scaled using the transform method
y_pred = model.predict(feature_scaler.transform(X_test))

# Evaluation
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n",
classification_report(y_test, y_pred, target_names=data.target_names))
