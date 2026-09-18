# Week 2 - Getting your Data Reacy For Analysis

* Evaluate the suitability of given data for use in analysis (MLO 2)
* Transform and clean simple tabular data using several common techniques (MLO 2)
* Extract and create features from simple tabular data (MLO 2)
* Integrate data from diverse sources (including multiple tables) (MLO 2)

### Lesson 1
Data is in the centre of any decision we make, but not all data is good data
* is it trustworthy, relevant, fit for the task at hand
* Can we rely on this data to support the conclusion we want to draw

Suitable data:
* Accuracy
* Completeness
* Ethical and Legal compliance
* Relevance
* Timeliness
* Accessibility

Accuracy and Reliability
* Data Correctness - are there any errors?
* Data credibility - who collected the original data, is it bias or limited
* Daa collection - How was it collected, are there any strengths or drawbacks here

Timeliness and Currency
* Is the data up to date? Older data might not be as relevant any more

How complete is the data set? Is anything missing?

Accessibility and format
* What are the licenses on the data
* HOw is it accessed? Is it locked down, behind a paywall?
* What format is the data in, such as a machine-readable format like JSON
* Is extra processing needed to import the data into your current workflow

Ethical and Legal responsibilities
* Are we legally allowed to use the data
* Are there any GDPR restrictions
* Any bias in datasets

Good decisions begin with good data
Access data thoroughly before analusis
Contextual suitability - what might be appropriate for one project might not be for another
Data is powerful when it's the right data

Analytics record = data set
data set = data relating to a collection of entities

DIKW pyramid (top to bottom)
* Wisdom - applied knowledge
* Knowledge - organised information
* Information - linked elements
* Data - abstracted elements
* World

ARFF files
----------
* Attribute-Relation File Format
* Used in WEKA
* Data cleaning will usually take a lot longer than data preparation
* Company-wide database integration = data warehousing
* XRFF - A version of ARFF that wraps it in XML
* `%` denotes a comment
* Attributes can be defined using the `@attribute` tag
* Strings can be escaped in the standard way `\"`

```arff
@relation weather

@attribute bag_ID {1, 2, 3, 4, 5, 6, 7}
@attribute bag relational
    @attribute outlook {sunny, overcast, rainy}
    @attribute temperature numeric
    @attribute humidity numeric
    @attribute windy {true, false}
@end bag
@attribute play? {yes, no}

@data
1, "sunny, 85, 85, false\nsunny, 80, 90, true", no
2, "overcast, 83, 86, false\nrainy, 70, 96, false", yes
```
Example from Fig 2.3 on page 88 of "Data Mining" by Ian H Witten et al

If there are values that default to zero, you can leave those out and just index
the fields you are populating. Ex:
`{1 X, 6, Y, 10 "class A"}

* Indexes start at 0 in ARFF
* Some values are missing because that's what the user is looking for
    * EX a doctor might do a test to see which value is missing to come up with a diagnosis
* Some data has rogue attributes/values, meaning the data wasn't collected originally
    * May have been considered unimportant at the time
    * Data may just change over time as well.

* Useful tools include histograms and distribution charts to visually see how the data looks

Examples:
* Missing values - Survey responses may refuse to answer specific questions such as age or income
* Inaccurate Values - People might make slight intentional errors to identify which data ends up
    being sold to advertisers, such as spelling in their address or extentions to their email
    address
* Unbalanced Values - Weather data for a location where it's predominantly one weather type, such
    as always raining in ireland.

### Lesson 2 - Cleaning Data
Five principles of dataa cleaning:
* You can't fix problems until you seee them
* Don't fix problems by making things worse
* Justify your fixes
* Sometimes you shouldn't fix
* At the end, acknowledge residual uncertainty (There is always residual uncertainty)

Undetected issues
- Suspiciously repeated values may be placeholders
- Some data might be filled in with averages instead of single data points

* Data Cleansing
    * Errors from data entry
    * Physically impossible values
    * missing values
    * outliers
    * spaces, typos
    * Errors against codebook(?)
* data transformation
    * aggregating data
    * Extrapolating data
    * derived measures
    * creating dummies
    * reducing number of variables
* combining data
    * merging/joining datasets
    * set operators
    * creating views

codebook = description of the data, a form of metadata
    * list value encodings for radiobutton style questions
    * what type of data (ex hierarchical, graph etc)

### Task 1
Look at the provided `gcse.arff` file and identify issues with the data
Write a bunch of rules to follow to clean up the data

* If <firstname is not uppercase> then <convert to uppercase>
* If <firstname contains whitespace> then <strip whitespace>
* if <len(firstname> le 3> then <remove row>
* if <lastname contains whitespace> then <strip whitespace>
* if <len(lastname) le 3>  then <remove row>
* if <gender[0].lower == 'm'> then <replace with "Male">
* if <gender[0].lower == 'f'> then <replace with "Female">
* If <dob out of range of 16-18 year olds taking their GCSE> then <remove row>
* If <subject is not wrapped in quotes> then <add quotes>
* If <grade is a number> then <replace with correct enumerated letter grade starting with A* = 1>
* If <grade letter out of range of predefined enumeration> then <replace with 'U' for lowest grade>
* If <grade is not supplied> then <set grade to U>
* If <subject is not present but grade is> then <remove row>
* If <subject and grade are both empty> then <do nothing>

### Lesson 3 -  Feature extraction and creation from tabular data
* Adding extra variables to a decision tree algorithm decreases accuracy
    * When running, this algorithm should select the most likely variable to switch on
    (which edge to follow to the next similar datum)
* Nearest Neighbor is highly susceptible to irrelevant attributes
    * One possibility is to use a decision tree first and strip out the attributes not used
    before passing into a nearest neighbor algorithm

Benefits of using subsets of data
* resulting models are easier to understand
* takes less computation

scheme dependant subsetting - applying planned learning algorithm to multiple potential subsets of
data and using the subset that has the best accuracy

Filter method - information gain ranking
    - filter methods use statistical properties like information gain or correlation evaluated
    independently of the model

### Lesson 4 - Data Integration
Merging multiple data sets isn't easy and takes up a lot of time

Integrating stages:
* extracting
* cleaning
* standardising
    - EX shoe sizes - using different numbeing systems around the world
* transforming
    - EX changing a raw age value into an age range because a difference by
    1 year (ex 42 YO vs 43 YO) rarely makes a difference
    - This is called binning
* integrating
    - Creating the analytics base table

Analytics Base Table - A table of data with redundant values removed
    - Used as input into ML algorithms
Analytics Record - An n x m matrix of n entities with m attributes
