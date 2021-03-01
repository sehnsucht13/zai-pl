# Copyright 2021 by Yavor Konstantinov <ykonstantinov1@gmail.com>

# This file is part of zai-pl.

# zai-pl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# zai-pl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with zai-pl. If not, see <https://www.gnu.org/licenses/>.

import argparse

from zai.vm import YAPL_VM
from pathlib import Path
from sys import exit


def main():
    vm = YAPL_VM()
    arg_parser = argparse.ArgumentParser(
        "yapl",
        description="An interpreter for yapl.",
        add_help="Interpreter for yapl",
    )
    arg_parser.add_argument(
        "file_path",
        nargs="?",
        help="File path leading to file to be interpreted.",
        default=None,
    )
    arg_parser.add_argument(
        "-e",
        "--eval_string",
        nargs=1,
        help="Evaluate a string and exit.",
        required=False,
        type=str,
    )

    args = arg_parser.parse_args()
    if args.eval_string is not None:
        vm.run_string(args.eval_string[0])
        exit(0)
    elif args.file_path is None:
        vm.run_repl()
        exit(0)
    else:
        f_path = Path(args.file_path)
        if f_path.exists() and f_path.is_file():
            file_text = f_path.open().read()
            # print(file_text)
            vm.run_string(file_text)
            exit(0)

        print("ERROR: path {} does not exist or is not a file.".format(args.file_path))
        exit(1)


if __name__ == "__main__":
    main()
