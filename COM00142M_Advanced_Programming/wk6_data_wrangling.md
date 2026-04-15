# Week 6 - Data Wrangling

* Apply data wrangling techniques for the grouping and reshaping of simple data sets
* Select and present the results of data analysis through appropriate visualisations
* Demonstrate the considerations required when handling time-series data.

### Lesson 1 - Data Wrangling
This is the term used by data scientists for the manipulation and reshaping of data
so that it provides an answer to a requirement. This occurs after the data has been 
cleaned

In pandas, you can provide a 2d array to the index key to create a multi-tier 
index for the data. This data can be turned into a "pivot table" by using pandas 
filtering and table drawing features

pivot table - a table of values which are aggregates of groups of vailes from a more
extensive table

Sometimes related data is stored/generated in different sources.
* `pandas.merge`
* `pandas.concat`
* `concat_first`

Once data sets have been grouped/merged, you can also reshape the data to be better 
presented. These are the pivot operations. Rows may be better as columns or vice versa.
This can often reveal missing data or inconsistencies.
* `pandas.stack`
* `pandas.unstack`
* `pandas.rotate`

### Lesson 2 - Data Visualisation
Once data has been cleaned and reshaped, the analysis process can begin. 
Types of visualisation:
* bar graph
* pie chart
* line graph
* histogram

Library in use - `matplotlib`

### Lesson 3 - Data Analysis
Data analysis process:
* information need (what you want to know)
* gather data (encoding, format, structure)
* clean data (missing data, consistency)
* reshape data (split, apply, combine)
* Analyse data (counts, statistics, correlations)
* present data (diagrams, graphs, gui)

Pandas has built in data types to handle times that work with the python standard
datetime libraries. This allows for slicing and other pandas-based benefits

Ways to refer to time-series data
* timestamps
* fixes periods (ex "Jan 2020")
* intervals of time (ex "every 5 minutes")
* experiment/elapsed time (relative to a start point)
