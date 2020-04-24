#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 24 October 2018
Purpose: Python program to write a Python program
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


# --------------------------------------------------
def get_args():
    """Get arguments"""

    parser = argparse.ArgumentParser(
        description='Create Python argparse program',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    defaults = get_defaults()

    parser.add_argument('program', help='Program name', type=str)

    parser.add_argument('-n',
                        '--name',
                        type=str,
                        default=defaults.get('name', os.getenv('USER')),
                        help='Name for docstring')

    parser.add_argument('-e',
                        '--email',
                        type=str,
                        default=defaults.get('email', ''),
                        help='Email for docstring')

    parser.add_argument('-p',
                        '--purpose',
                        type=str,
                        default='Rock the Casbah',
                        help='Purpose for docstring')

    parser.add_argument('-f',
                        '--force',
                        help='Overwrite existing',
                        action='store_true')

    args = parser.parse_args()

    args.program = args.program.strip().replace('-', '_')

    if not args.program:
        parser.error(f'Not a usable filename "{args.program}"')

    if args.email:
        args.email = f'<{args.email}>'

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    program = args.program

    if os.path.isfile(program) and not args.force:
        answer = input(f'"{program}" exists.  Overwrite? [yN] ')
        if not answer.lower().startswith('y'):
            print('Will not overwrite. Bye!')
            sys.exit()

    text = body(name=args.name,
                email=args.email,
                purpose=args.purpose,
                date=str(date.today()))

    print(text, file=open(program, 'wt'), end='')
    subprocess.run(['chmod', '+x', program])
    print(f'Done, see new script "{program}."')


# --------------------------------------------------
def preamble(**args):
    return f"""#!/usr/bin/env python3
\"\"\"
Author : {args['name']}{' <' + args['email'] + '>' if args['email'] else ''}
Date   : {args['date']}
Purpose: {args['purpose']}
\"\"\"
"""


# --------------------------------------------------
def body(**args):
    """ The program template """

    return f"""#!/usr/bin/env python3
\"\"\"
Author : {args['name']}{args['email']}
Date   : {args['date']}
Purpose: {args['purpose']}
\"\"\"

import argparse
import os
import sys


# --------------------------------------------------
def get_args():
    \"\"\"Get command-line arguments\"\"\"

    parser = argparse.ArgumentParser(
        description='{args["purpose"]}',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('positional',
                        metavar='str',
                        help='A positional argument')

    parser.add_argument('-a',
                        '--arg',
                        help='A named string argument',
                        metavar='str',
                        type=str,
                        default='')

    parser.add_argument('-i',
                        '--int',
                        help='A named integer argument',
                        metavar='int',
                        type=int,
                        default=0)

    parser.add_argument('-f',
                        '--file',
                        help='A readable file',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        default=None)

    parser.add_argument('-o',
                        '--on',
                        help='A boolean flag',
                        action='store_true')

    return parser.parse_args()


# --------------------------------------------------
def main():
    \"\"\"Make a jazz noise here\"\"\"

    args = get_args()
    str_arg = args.arg
    int_arg = args.int
    file_arg = args.file
    flag_arg = args.on
    pos_arg = args.positional

    print(f'str_arg = "{{str_arg}}"')
    print(f'int_arg = "{{int_arg}}"')
    print('file_arg = "{{}}"'.format(file_arg.name if file_arg else ''))
    print(f'flag_arg = "{{flag_arg}}"')
    print(f'positional = "{{pos_arg}}"')


# --------------------------------------------------
if __name__ == '__main__':
    main()
"""


# --------------------------------------------------
def get_defaults():
    """Get defaults from ~/.new.py"""

    rc = os.path.join(str(Path.home()), '.new.py')
    defaults = {}
    if os.path.isfile(rc):
        for line in open(rc):
            match = re.match('([^=]+)=([^=]+)', line)
            if match:
                key, val = map(str.strip, match.groups())
                if key and val:
                    defaults[key] = val

    return defaults


# --------------------------------------------------
if __name__ == '__main__':
    main()
