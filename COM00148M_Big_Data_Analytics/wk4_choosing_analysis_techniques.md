# Week 4 - Choosing an Analysis Technique

* Apply multiple regression and support vector regression. [MLO 3]
* Apply Naïve Bayes and support vector classification. [MLO 3]
* Choose between techniques for a given analysis in a principled way. [MLO 3]
* Identify, address and document residual threats to validity for a given analysis. [MLO 3]

### Lesson 1
* Multiple linear regression
* Kernel Ridge regression
* Support Vector regression

MLR - In multiple linear regression, we have multiple dependant values
    - To calculate the slope needed, we instead add together every value multiplied by a weight
    y = W0 + W1X1 + W2X2 etc
    - We also add in an intercept, usually W0
    - For each data point, we use MSE to calculate the error. We want to find the set of weights
    that minimises the total squared error.

Evaluating model performance - often uses Residual Sum of Squares (RSS) calculation
    -total squared difference between actual values and model predictions
    - Alternative is Rsquared, varince in dependant variable in range 0-1

Support Vector machine
    - Finds the maxinmim margin hyperplane
        - hyperplane = liner model
    - SVMs are often used in classification problems, they find the optimal space between data
        points of opposite classes
    - Widely used for machine learning as it can be used for both linear and nonlinear
    classification tasks
    - This gets more complicated when the data isn't linearly separable.
    - Support vector regression is a form of SVM applied to regression problems
        ( The outcome is continuous)
        - typically used for time series predictions. The example in the IBM article is of
        identifying cars in an image of a motorway with a camera

Multicolinearity - when two variables have very similar values, but aren't actually related
    - Ex number of bathrooms in a house and number of bedrooms.

Ordinary least squares (OLS) - calculation to estimate coefficients
    - High value can be a sign of overfitting

Kernel ridge regression
    - Can be calulcated as a weighted sum of the dot products of each training instance
    - Ridge Regression will shrink the coefficients down and reduce the OLS value
        - Different coefficients will be reduced by different amounts, not uniformly


