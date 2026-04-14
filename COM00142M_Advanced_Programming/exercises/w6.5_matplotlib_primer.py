import numpy
import matplotlib.pyplot as plt

data = numpy.arange(10)
plt.plot(data)
# The plot should just show up here as a straight line, but wouldn't open on 
# any platform I could access, even with `plt.show()`

# plots reside within a figure object
# Subplots are graphs within the plot space
fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)  # dimensions are 2x2, we're setting the first subplot
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)

# line graph
ax3.plot(
    numpy.random.standard_normal(50).cumsum(),
    color="black",
    linestyle="dashed"
)

ax1.hist(
    numpy.random.standard_normal(100).cumsum(),
    bins=20,
    color="black",
    alpha=0.3  # style option, sets opacity of the plot
)

ax2.scatter(
    numpy.arange(30),
    numpy.arange(30) + 3 * numpy.random.standard_normal(30)
)

fig, axes = plt.subplots(2,3)
# axes is a numpy array of subplot objects
