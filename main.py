import sys

import matplotlib

import calories
import eat_counts
import magnesium
import creatine


font = {"family": "monospace", "weight": "normal", "size": 18}

matplotlib.rc("font", **font)


def main():
    dir_path = sys.argv[1]
    print("Plotting calories")
    calories.plot(dir_path)
    print("Plotting eat counts")
    eat_counts.plot(dir_path)
    print("Plotting magnesium")
    magnesium.plot(dir_path)
    print("Plotting creatine")
    creatine.plot(dir_path)


if __name__ == "__main__":
    main()
