import pandas

def exercise_one():
    with open("collegeGrades1.csv") as f:
        # strip lines that are only full of commas (empty lines)
        lines = [l.strip() for l in f.readlines() if len(set(l)) > 2]

    # table 1
    header = [x for x in lines[1].split(",") if x]
    print(header)

if __name__ == "__main__":
    raise SystemExit(exercise_one())
