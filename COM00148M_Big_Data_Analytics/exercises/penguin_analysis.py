# Week 4 task
import pandas
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Step 1, perform visualisation using a decision tree

def display_decision_tree(tree, features_encoded):
    plt.figure(figsize=(12, 6))
    plot_tree(
        tree,
        feature_names=features_encoded.columns,
        class_names=tree.classes_,
        filled=True
    )
    plt.show()

def create_decision_tree(penguin_data):

    features = penguin_data.iloc[:, 1:]
    output = penguin_data.iloc[:, 0]

    # turn categorical features into numeric values
    features_encoded = pandas.get_dummies(features)

    features_train, features_test, output_train, output_test = train_test_split(
        features_encoded,
        output,
        random_state=0,
        test_size=0.4
    )

    decision_tree = DecisionTreeClassifier(
        criterion="entropy",
        splitter="best",
        random_state=0
    )

    decision_tree.fit(features_train, output_train)

    display_decision_tree(decision_tree, features_encoded)
    return decision_tree


# Step 2: predict the body mass of a penguin based on it's bill size
def prediction(penguin_data):
    independant = penguin_data[["body_mass_g"]]
    dependant = penguin_data["bill_depth_mm"]
    model = LinearRegression()
    model.fit(independant, dependant)

    print(f"Intercept: {round(model.intercept_,2)}")
    print(f"Coefficient: {round(model.coef_[0],2)}")

penguin_data = pandas.read_csv("penguins.csv", delimiter=',', encoding="utf-8")
create_decision_tree(penguin_data)
prediction(penguin_data)


