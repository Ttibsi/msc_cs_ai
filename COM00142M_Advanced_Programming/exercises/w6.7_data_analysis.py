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

### time series
import datetime
datestrs = ["2011-07-06 12:00:00", "2011-08-06 00:00:00"]
times = pandas.to_datetime(datestrs)
# Also registers "NaT" (not a time)
not_a_time = pandas.to_datetime([None])

# timeseries is a series of time values
ts = pandas.Series(numpy.random.standard_normal(2), index=datestrs)
# print(ts)

# indexing can use subscripting to get the date based on a date string
longer_ts = pandas.Series(
    numpy.random.standard_normal(1000),
    index=pandas.date_range("2000-01-01", periods=1000)
)
# print(longer_ts["2001"])
# print(longer_ts["2001-05"])
# print(longer_ts.truncate(after="2011-01-09"))
# print(longer_ts.is_unique)

# pandas can generate daily timestamps on a given range
daily = pandas.date_range(start="2012-04-01", periods=20)
print(daily)
