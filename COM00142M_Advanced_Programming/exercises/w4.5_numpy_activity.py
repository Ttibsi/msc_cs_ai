import csv
import numpy

def exercise_one():
    arr = numpy.random.random((10000, 10000))
    root = numpy.sqrt(arr)
    print(numpy.sum(arr))


def exercise_two():
    file = numpy.genfromtxt("RandomValues.csv", delimiter=",")
    first = file[5:10:2]
    second = file[[0,7,10], :]
    #third = file[0,7:, numpy.newaxis, : 3,10]
    third = file[7:9+1, 1:3]

    print(third)


def exercise_three():
    with open("SalesData.csv") as f:
        reader = csv.reader(f)
        headers = next(reader)
        contents = list(reader)

    row_headers = [x[0] for x in contents]
    remaining = []
    for x in contents:
        remaining.append([int(y) for y in x[1:]])
    arr = numpy.array(remaining)

    # start at col 4 to col 7
    sec_quarter = arr[0:, 3:6]
    print(sec_quarter)
    totals = sec_quarter.sum(axis=0)
    means =  sec_quarter.mean(axis=0)
    print(f"Totals = {totals}")
    print(f"Mean = {means}")

    l3_l1 = arr[1:3, ]
    print(l3_l1)
    totals = l3_l1.sum(axis=0)
    means =  l3_l1.mean(axis=0)
    print(f"Totals = {totals}")
    print(f"Mean = {means}")

    n_stores = arr[3:5, ]
    print(n_stores)
    under_400 = []
    for elem in n_stores:
        for idx, x in enumerate(elem):
            if x < 400:
                print(f"Month: {headers[idx +1]}, value: {x}")


def exercise_four():
    island = [0,0,0,1,0,0,0]
    walk = numpy.random.choice([-1, 1], size=1000)
    position = numpy.cumsum(walk)
    print(position)


if __name__ == "__main__":
    raise SystemExit(exercise_four())
