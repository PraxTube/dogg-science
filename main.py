import sys

import calories
import eat_counts


def main():
    dir_path = sys.argv[1]
    calories.plot(dir_path)
    eat_counts.plot(dir_path)


if __name__ == "__main__":
    main()
