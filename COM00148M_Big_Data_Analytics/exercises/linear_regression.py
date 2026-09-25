import pandas
from sklearn.linear_model import LinearRegression

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
