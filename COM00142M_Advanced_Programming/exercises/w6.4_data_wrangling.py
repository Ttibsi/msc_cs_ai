import pandas

def exercise_one():
    with open("collegeGrades1.csv") as f:
        # strip lines that are only full of commas (empty lines)
        lines = [l for l in f.readlines() if len(set(l)) > 1]
        headings = lines[0:2]
        body = [l.strip().split(",") for l in lines[2:]]
        indexes = [l[0] for l in body if l[0]]

    data = pandas.DataFrame(body)
    print(data)


    # data = pandas.read_csv("collegeGrades1.csv")
    # data.dropna(how="all", inplace=True)
    # data = data.set_index([0, 1])
    # print(data)

if __name__ == "__main__":
    raise SystemExit(exercise_one())
