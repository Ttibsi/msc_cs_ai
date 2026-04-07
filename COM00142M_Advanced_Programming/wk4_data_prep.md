# Week 4 - Data Preparation

* Identify mathematical terms and techniques associated with the preparation and analysis of data
* Articulate the advantages and disadvantages of using constructs from the NumPy and pandas' APIs within specific contexts
* Select and apply appropriate NumPy and pandas' data structures and functions to solve simple data cleaning and organisation problems.

# Mathematics refresher
* Mean - Add all values and divide by amount of values
* Mode - Most common value
* Median - If we order a set of data from lowest to highest, the median is the
    point that divides the scores into two.
* Range - difference between the highest and lowest values
* Quartile - If we order a set of scores from lowest to highest, the quartiles
    are the points that divide the scores into 4 equal groups
* Deviation - Difference of a score from the mean
* Standard deviation - the average deviation of all scores from the mean.
* Variance - Measure of how many a set of scores vary by from their mean.
    Variance is the square of of the standard deviation

* Linear Correlation - How close the relationship between two variables are
* Linear Regression -  The straight line that best describes the linear
    relationship between two variables.

### Lesson 1 - NumPy
NumPy is a library for cleaning and analysing very large data sets with more efficiency than
standard python data structures. Numpy includes:
* A high-performance multidimensional array: `ndarray`
* Functions for generating random values
* Data Types for to express `Scalar` and `dtype` values
* Mathematical functions
* Specialised mathematical techniques

Numpy arrays must contain the same type, unlike lists which can hold different types
Vectorisation is the term for performing arithmetic operations on all lines in an array
Numpy Arrays are efficient because they store data in contiguous blocks of memory

Element-wise product - multiplying two matrices together

### Lesson 2 - Pandas
Pandas provides specialised data structures: `Series` and `DataFrame` classes
    - Series are for handling KV pair data
    - DataFrames are for handling data with row and column headers

numpy `ndarray` is more suited to homogenous data, pandas is better for handling
tabulated data

### Lesson 3 - Prep for data analysis
Serialization - the process of storing and retrieving objects to and from a binary representation.
In python, the pickle library handles this

Cleaning data
* removing missing data
* removing duplicate data
* replacing values 
* renaming axis
* discretization and binning
* removing outliers
