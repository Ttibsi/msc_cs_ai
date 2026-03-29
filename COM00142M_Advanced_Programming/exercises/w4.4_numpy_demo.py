import numpy
# Create a 2x3 matrix
data = numpy.random.randn(2, 3)
# print(data)

# Perform basic maths on every element
data = data * 10
# print(data)

# arr = numpy.array([6, 7.5, 8, 0, 1])
# Nested arrays will become 2 dimensional
arr = numpy.array([[6, 7.5, 8, 0, 1],[2,4,6,8,9]])
# print(arr)

# Or zero-out an array
zeroes = numpy.zeros(3)
# empty = numpy.empty((2,3,2))
# print(empty)

arr = numpy.array([6, 7.5, 8, 0, 1])
# print(6 in arr)
# propagate new values
arr[1:3] = 12
# print(arr)
# or every value
# arr[:] = 12
# print(arr)


