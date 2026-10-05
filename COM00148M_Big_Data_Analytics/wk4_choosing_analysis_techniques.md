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
    - Primary objective is to predict a numeric value using multiple independant variables

Evaluating model performance - often uses Residual Sum of Squares (RSS) calculation
    -total squared difference between actual values and model predictions
    - Alternative is Rsquared, varince in dependant variable in range 0-1

Support Vector machine
    - Finds the maximum margin hyperplane
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

### Lesson 2 - Alternatives for Classification
Naive Bayes Modelling
    - Used for classification (spam/not spam)
    - "class-conditional independence assumption"
    - conditional probabilities of features given each class
    - prior probabilities for each class

Bayesian Statistics
    - rooted in Bayes theorem, a fundamental property of probability theory
    - Allows us toe continuously update our beliefs based on fresh evidence

`P(A|B) = (P(B|A) * P(A)) / P(B)` where `P` is the probability of A or B

Reminder that in set theory, doing `P(A|B)` means that it's the possibility of A in the
dataset of B.
    - Good explanation of this formula is in the youtube video `Naive Bayes, Clearly Explained`
    by `Statquest with josh starmer`

Why naive - the assumption that all features are independant once you know the category
    - ex in spam detection, each word in the email doesn't affect other words
    - ex in a factory producing bottles, one defective bottle doesn't affect the others

Which classifiers to use
    - gaussian naive bayes - assumes the data follows a normal distribution and is best for
                            continuous data
    - multinomial naive bayes - great for text classification, words are counted to assign
                                documents to categories
    - Bernoulli naive bayes - works well on binary data, meaning features only have two possible
                            values.

### Lesson 3 - Choosing a learning technique
3 step approach
    1 - Identify the techniques that are appropriate (classification, regression, clustering)
    2 - Quantitative performance - which are likely to perform best in terms of accuracy,
                                    error rate etc.
    3 - Empirical testing - If you still have multiple techniques in mind, use them all and see
                            which gets you the best results. This can be done with smaller
                            subsets of the data for faster iteration to start

* When thinking about performance, you also need to think about technical limitations
    - What kind of models can be trained fast enough with the hardware you have, for example
* How will you handle outliers?

* Feature engineering
* Algorithm selection
* parameter tuning

---
* Residual - difference between observed and predicted values
* Naive bayes independance assumption does not need to hold exactly
    - well suited to social media post sentiment analysis, spam filtering in emails, document classification
* SVC and decision trees
* SVR and KRR
