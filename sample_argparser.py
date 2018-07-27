import argparse
from ast import literal_eval


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='hahahaaaa')
    parser.add_argument('--ratio', '-r', type=float, default=1.0, help='ratio')
    parser.add_argument('--str', '-s', type=str, help="some string")
    parser.add_argument('--do_shuffle', '-S', action="store_true", default=False)

    args = parser.parse_args()

    if args.ratios:
        print args.ratios, type(args.ratios)
