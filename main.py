import argparse
import os
import zipfile

from zip_fs.command import (
    Command, PWDCommand, LSCommand, CDCommand, CATCommand
)


def check_zip(path):
    if os.path.isfile(path):
        try:
            _ = zipfile.ZipFile(path)
            return path
        except zipfile.BadZipFile:
            raise argparse.ArgumentTypeError(
                f"Wrong file is given"
            )
    else:
        raise argparse.ArgumentTypeError(
            f"Given path is not zip archive"
        )


def get_command(input_str: str) -> Command:
    # this solution is very simple and can be much more difficult
    parameters = input_str.split(' ')
    program = parameters[0]
    parameters = parameters[1:]
    if program == "pwd":
        return PWDCommand()
    elif program == "ls":
        return LSCommand()
    elif program == "cd":
        return CDCommand("".join(parameters))
    elif program == "cat":
        return CATCommand("".join(parameters))
    elif program == "exit":
        print("Goodbye!")
        return None
    else:
        raise ValueError("This is not a valid command")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="path", type=check_zip,
        help="path to the zip archive"
    )
    parsed_args = parser.parse_args()
    path = parsed_args.path
    # path = "example/example.zip"

    with zipfile.ZipFile(path, "r") as archive:
        cur_path = zipfile.Path(archive)
        while True:
            try:
                command = get_command(input('-> '))
            except ValueError as e:
                print(str(e))
                continue
            if command is None:
                break
            cur_path = command.run(archive, cur_path)


if __name__ == "__main__":
    main()
