import pandas
from scipy import stats
from pandas.plotting import table 
import matplotlib.pyplot as plt

def ftoc(val: float) -> float:
    return 5 / 9 * (val - 32)

def write_image(frame: pandas.DataFrame):
    ax = plt.subplot(111)
    table(ax, frame)
    plt.savefig("mytable.png")

def main() -> int:
    lines = []
    with open("nyc-temps.csv", "r") as f:
        lines = f.readlines()

    temps: list[int] = [(f, ftoc(f)) for f in range(0, 101, 10)]
    temps_df = pandas.DataFrame(temps, columns=["Fahrenheit", "Celsius"])
    axes = temps_df.plot(x="Fahrenheit", y="Celsius", style=".-")
    y_label = axes.set_ylabel("Celsius")

    averages = [x.split(",")[1] for x in lines]

    # stats.linregress()

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
