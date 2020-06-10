import argparse
from vm import VM
from pathlib import Path


def main():
    vm = VM()
    arg_parser = argparse.ArgumentParser(
        "yapl", description="An interpreter for yapl.", add_help="Interpreter for yapl",
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
    elif args.file_path is None:
        vm.run_repl()
    else:
        f_path = Path(args.file_path)
        if f_path.exists() and f_path.is_file():
            file_text = f_path.open().read()
            print(file_text)
            vm.run_string(file_text)


if __name__ == "__main__":
    main()
