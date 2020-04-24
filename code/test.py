#!/usr/bin/env python3
"""tests for add.py"""

import os
import random
import string
import re
from subprocess import getstatusoutput, getoutput

prg = './add.py'


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_wrong_number_args():
    """test for wrong number of arguments"""

    for k in [0, 1, 3]:
        args = ' '.join(map(str, random.sample(range(10), k=k)))
        rv, out = getstatusoutput(f'{prg} {args}')
        assert rv != 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_not_numbers():
    """test for not providing numbers"""

    bad = random_string()
    args = [str(random.choice(range(10))), bad]

    for _ in range(2):
        args = list(reversed(args))
        rv, out = getstatusoutput(f'{prg} {" ".join(args)}')
        assert rv != 0
        assert out.lower().startswith('usage')
        assert re.search(f"invalid int value: '{bad}'", out)


# --------------------------------------------------
def test_valid_input():
    """test with valid input"""

    for x, y, z in [[0, 0, 0], [1, 0, 1], [1, 2, 3], [2, 1, 3]]:
        rv, out = getstatusoutput(f'{prg} {x} {y}')
        assert rv == 0
        assert out.rstrip() == f'{x} + {y} = {z}'


# --------------------------------------------------
def random_string():
    """generate a random string"""

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
