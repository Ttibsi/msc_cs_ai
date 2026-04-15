import pandas
import numpy

df = pandas.DataFrame({
    "key1" : ["a", "a", None, "b", "b", "a", None],
    "key2" : pandas.Series([1, 2, 1, 2, 1, None, 1], dtype="Int64"),
    "data1" : numpy.random.standard_normal(7),
    "data2" : numpy.random.standard_normal(7)
})

# We can group one key by another key
grouped = df["data1"].groupby(df["key1"])
# print(grouped.mean())

# or by a series
states = numpy.array(["OH", "CA", "CA", "OH", "OH", "CA", "OH"])
years = [2005, 2005, 2006, 2005, 2006, 2005, 2006]
x = df["data1"].groupby([states, years]).mean()
# print(x)

# Missing values can be excluded by default, but dropna=false can prevent this
# print(df.groupby("key1", dropna=False).size())

# Or you can shortcut things like this:
df.groupby("key1")["data1"] == df["data1"].groupby(df["key1"])

