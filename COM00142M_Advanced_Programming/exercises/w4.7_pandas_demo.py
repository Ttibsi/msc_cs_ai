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

# Indexing
idx = pandas.Series(range(3), index=['a', 'b', 'c'])
print(idx)
print(idx.index)

# Reindex to sort in a different order
idx2 = idx.reindex(['c', 'b', 'a'])
print(idx2)

# These column headers don't exist, but you can reindex a frame too
print(df.reindex(columns=['foo', 'bar', 'baz']))

# indexing, selection, filtering
print("---")
print(df["pop"])
print(df.T[0])
print(df[["pop", "state"]])
print("---")
print(df["pop"][1:3])

print("---")
import numpy
data = pandas.Series(numpy.arange(6.))
print(data[3])
