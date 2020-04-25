#!/usr/bin/env python3
"""Add two integer values"""

import argparse


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Add two integer values',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('numbers',
                        metavar='int',
                        nargs=2,
                        type=int,
                        help='Two numbers to add')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    n1, n2 = args.numbers
    print(f'{n1} + {n2} = {n1 + n2}')


# --------------------------------------------------
if __name__ == '__main__':
    main()
