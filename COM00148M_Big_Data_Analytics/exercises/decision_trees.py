import pandas
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

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
    random_state=0,
    test_size=0.4
)

# decision tree time
decision_tree = DecisionTreeClassifier(
    criterion="entropy",
    splitter="best",
    random_state=0
)

decision_tree.fit(features_train, output_train)

# display tree
plt.figure(figsize=(12, 6))
plot_tree(
    decision_tree,
    feature_names=features_encoded.columns,
    class_names=decision_tree.classes_,
    filled=True
)
plt.show()
