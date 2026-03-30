import pandas

# Series is a 1D array object, you can set the index of each element
obj = pandas.Series([4,7,-5,3], index=['d', 'c', 'b', 'a'])
# Set the column headers
obj.name = "value"
obj.index_name = "letter"
print(obj)
print(obj['a'])

# You can still reach the numerical index of each element
print(obj[obj > 0])

# Or multiply each element
print(obj * 2)


# DataFrames are fancy 2d dicts
data = {
    'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
    'year': [2000, 2001, 2002, 2001, 2002, 2003],
    'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]
}
cols = ["year", "state", "pop"] # and you can define the order of headers shown
df = pandas.DataFrame(data, columns=cols)
print(df.head()) # Just printing the head will show the first 5 rows
print(df["year"]) # print the year as a Series
print(df.T) # Rotate rows and columns
