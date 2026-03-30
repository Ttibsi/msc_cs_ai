import pandas

def exercise_one():
    a_list = [1,2,3,4]
    a_series = pandas.Series(a_list)
    print(a_series)

    a_dict = {"foo": [1,2], "bar": [3,4], "baz": [5,6]}
    a_df = pandas.DataFrame(a_dict)
    print(a_df)


def exercise_two():
    file = pandas.read_csv("SalesData.csv")
    print(file.iloc[[2, 5], [2, 11, 12]])

    print(file.iloc[[1,0], [6,7,8]].pct_change())
    top_three = file.iloc[[3,4]].stack().nlargest(2)
    print(top_three)


if __name__ == '__main__':
    raise SystemExit(exercise_two())
