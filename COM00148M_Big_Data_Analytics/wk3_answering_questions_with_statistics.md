# Week 3 - Answering questions with statistics and Machine Learning

* Apply some basic descriptive statistics (MLO 2)
* Explain the concepts of classification and regression (MLO 3)
* Apply linear regression to reasonably clean data (MLO 3)
* Apply decision trees to reasonably clean data (MLO 3)
* Evaluate classification and regression models using simple standard metrics (MLO 3)

### Lesson 1
Introduction to descriptive statistics
* Summary statistics are one way to show the results of a study
* Visualisation is the other way, and can be used to show more information
* Visualisation also makes the data clearer to see comparisons

* Bar chars
* Histogram - grouping data based on a value
    - Each bar in a histogram is called a bin
    - Values that lie on the bin boundary are counted as part of the lower bin
* Scatter plots - good for visualising two variables

The mean of a range of values is usually represented as an `x` with a line overtop
The mode (most common) is not always obvious and might not matter in all scenarios

deviation - the distance of a value from the mean
variance - square the deviations and take an average
    - denoted by `s^2`
standard deviation - sqrt(variance)

box plots
* Find the median value(s)
    - If there are an even amount of values, add the two middle values together
    and divide by 2
* IQR - interquartile range
    - IQR = 75th percentile subtract 25th percentile
* upper/lower whisker = 1.5*IQR
    - These attempt to capture the data outside the box made by
    the IQR
    - Anything else is an outlier

When data is strongly skewed, it's sometimes transformed so it's easier to model
EX using log10(population) instead of the whole population when displaying on a histogram
There are standardised transformations that should be kept to
    * log10
    * sqrt

Contingency tables are tables that have headings along both the top and LHS
They often show the relationship/association between two different categories
(google it)
