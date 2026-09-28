import pandas
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Import data
possum_data = pandas.read_csv("possum.csv", delimiter=",", encoding="utf-8")
independant = possum_data[["totalL"]]
dependant = possum_data["headL"]

# Train a model
model = LinearRegression()
model.fit(independant, dependant)

print(f"Intercept: {round(model.intercept_,2)}")
print(f"Coefficient: {round(model.coef_[0],2)}")

# request output with given input values
test = pandas.DataFrame({"totalL":[70, 80, 85]})
prediction = model.predict(test)
print(prediction)

# Split the data into training and testing data
for split in [0.8, 0.7, 0.6, 0.5]:
    X_train, X_test, y_train, y_test = train_test_split(independant, dependant, test_size=split, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # evaluate
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print('-----------------------------------------------------------------')
    print(f'For a split of {round((1-split)*100)}% training',
          f'/ {round(split*100)}% test the model is:',
          f' y = {round(model.intercept_,2)} + {round(model.coef_[0],2)} x.')
    print(f"Mean Squared Error (MSE): {mse:.3f}")
    print(f"Mean Absolute Error (MAE): {mae:.3f}")
    print(f"R² Score: {r2:.3f}")
    print('-----------------------------------------------------------------')

# Cross validation
scoring = ['neg_mean_absolute_error', 'neg_mean_squared_error', 'r2']
folds = len(scoring)
results = cross_validate(
    model,
    independant,
    dependant,
    cv=folds,
    scoring=scoring,
    return_estimator=True
)

for i in range(folds):
    print('-----------------------------------------------------------------')
    print(f"Fold {i+1} y = {results['estimator'][i].coef_} x +",
    f"{results['estimator'][i].intercept_}")
    print("MSE per fold:", -results['test_neg_mean_squared_error'][i])
    print("MAE per fold:", -results['test_neg_mean_absolute_error'][i])
    print("R² per fold:", results['test_r2'][i])
    print('-----------------------------------------------------------------')
