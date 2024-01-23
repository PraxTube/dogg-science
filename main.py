import sys

import calories
import eat_counts
import magnesium


def main():
    dir_path = sys.argv[1]
    print("Plotting calories")
    calories.plot(dir_path)
    print("Plotting eat counts")
    eat_counts.plot(dir_path)
    print("Plotting magnesium")
    magnesium.plot(dir_path)


if __name__ == "__main__":
    main()
