import pandas

def exercise_one():
    a_list = [1,2,3,4]
    a_series = pandas.Series(a_list)
    print(a_series)

    a_dict = {"foo": [1,2], "bar": [3,4], "baz": [5,6]}
    a_df = pandas.DataFrame(a_dict)
    print(a_df)


def exercise_two():
    with open ("SalesData.csv") as f:
        lines = f.readlines()
        columns = lines[0].strip().split(",")[1:]
        rest = [l.strip().split(",") for l in lines[1:]]
        index = [i[0] for i in rest]
        body = [i[1:] for i in rest]
        body = [[int(item) for item in row] for row in body]

    file = pandas.DataFrame(body, columns=columns, index=index)
    print(file)
    ret_1 = file.loc[["P2", "B8"], ["Nov-18", "Feb-19", "Mar-19"]]
    print(f"Sales (P2/B8):\n {ret_1}")
    
    ret_2 = file.loc[["L3", "L1"], ["Oct-18", "Nov-18", "Dec-18"]]
    print(f"Third quarter:\n {ret_2}")
    print(f"Percentage increase:\n {ret_2.pct_change()}")

    ret_3 = file.loc[["N6", "N4"]].stack().nlargest(3)
    print(f"top ny stores:\n {ret_3}")

    ret_4 = file.min().min()
    print(f"Lowest values:\n {ret_4}")


def exercise_three():
    with open ("SalesData.csv") as f:
        lines = f.readlines()
        columns = lines[0].strip().split(",")[1:]
        rest = [l.strip().split(",") for l in lines[1:]]
        index = [i[0] for i in rest]
        body = [i[1:] for i in rest]
        body = [[int(item) for item in row] for row in body]

    file = pandas.DataFrame(body, columns=columns, index=index)
    pct = file.pct_change()
    print(f"Max: {pct.max()}")
    print(f"Min: {pct.min()}")

if __name__ == '__main__':
    raise SystemExit(exercise_three())
