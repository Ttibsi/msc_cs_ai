import pandas
import numpy

from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def root_relative_squared_error(y_true, y_pred):
    numerator = numpy.sum((y_true - y_pred) ** 2)
    denominator = numpy.sum((y_true - numpy.mean(y_true)) ** 2)
    return numpy.sqrt(numerator / denominator)

def relative_absolute_error(y_true, y_pred):
    numerator = numpy.sum(numpy.abs(y_true - y_pred))
    denominator = numpy.sum(numpy.abs(y_true - numpy.mean(y_true)))
    return numerator / denominator

# Import data
possum_data = pandas.read_csv("possum.csv", delimiter=",", encoding="utf-8")
possum_encoded = pandas.get_dummies(possum_data)

features_data = possum_encoded[['site', 'age', 'headL', 'skullW ', 'totalL', 'sex_m', 'sex_f']]
target_data = possum_encoded["tailL"]
X_train, X_test, y_train, y_test = features_data, features_data, target_data, target_data

# Linear regression
LRmodel = LinearRegression()
LRmodel.fit(X_train, y_train)

# Standard features for SVR
feature_scaler = StandardScaler()
X_train_scaled = feature_scaler.fit_transform(X_train)
target_scaler = StandardScaler()
y_train_scaled = target_scaler.fit_transform(y_train.values.reshape(len(y_train),1))

# Support Vector Regression
svr_model = SVR(kernel='rbf', C=1.0, epsilon=0.1)
svr_model.fit(X_train_scaled, numpy.reshape(y_train_scaled, len(y_train_scaled)))

# Evaluating models
lr_pred = LRmodel.predict(X_test)
# Note the same scaling needed to happen here as did to the training data
svr_pred = svr_model.predict(feature_scaler.transform(X_test))
# and then reverse the scaling
svr_pred = target_scaler.inverse_transform(svr_pred.reshape(-1, 1)).flatten()

split_sizes = [0.2, 0.3, 0.4, 0.5]
for size in split_sizes:
    print(f'######### Percentage Split: {round(size*100)}% #########')

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features_data, target_data,
    test_size=size, random_state=19)

    # Create and train the Linear Regression model
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)

    # Predict for Linear Regression Model
    lr_pred = lr_model.predict(X_test)
    print('---------------- LR Model -----------------------------')
    print("RRSE:", root_relative_squared_error(y_test, lr_pred))
    print("RAE:", relative_absolute_error(y_test, lr_pred))
    print("RMSE:", numpy.sqrt(mean_squared_error(y_test, lr_pred)))
    print("R² score:", r2_score(y_test, lr_pred))
    print('MSA:', mean_absolute_error(y_test, lr_pred))

    # Standardising features for SVR
    feature_scaler = StandardScaler()
    X_train_scaled = feature_scaler.fit_transform(X_train)
    # Standardising target SVR
    target_scaler = StandardScaler()
    y_train_scaled = target_scaler.fit_transform(
    y_train.values.reshape(len(y_train),1))

    # Create and train the SMOreg equivalent model
    svr_model = SVR(kernel='rbf', C=1.0, epsilon=0.1)
    svr_model.fit(X_train_scaled, numpy.reshape(y_train_scaled, len(y_train_scaled)))

    # Predict for SVR Model
    svr_pred = svr_model.predict(feature_scaler.transform(X_test))

    # Inverse the transform on the predicted value so it can be compared to the
    # real data.
    svr_pred = target_scaler.inverse_transform(svr_pred.reshape(-1, 1)).flatten()
    print('---------------- SVR Model -----------------------------')
    print("RRSE:", root_relative_squared_error(y_test, svr_pred))
    print("RAE:", relative_absolute_error(y_test, svr_pred))
    print("RMSE:", numpy.sqrt(mean_squared_error(y_test, svr_pred)))
    print("R² score:", r2_score(y_test, svr_pred))
    print('MSA:', mean_absolute_error(y_test, svr_pred))
