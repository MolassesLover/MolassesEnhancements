# region Modules

import argparse
import colorama
from colorama import Fore
import subprocess
from subprocess import check_output
import os
import sys

# endregion

# region Functions


def format(
    command: str,
    extension: str,
    language: str,
    sourcePath: str,
    output: bool,
    fileAmount: bool,
):
    for root, dirs, files in os.walk(sourcePath):
        for file in files:
            if file.lower().endswith(extension.lower()):
                print(
                    f":: {Fore.BLUE}Formatting{Fore.RESET} {Fore.YELLOW}{file}{Fore.RESET} as {Fore.GREEN}{language}{Fore.RESET}"
                )
                try:
                    subprocess.check_output(
                        f"{command} {os.path.join(root, file)}",
                        shell=True,
                    )
                    if output:
                        subprocess.check_output(
                            f"{command} {os.path.join(root, file)}",
                            shell=True,
                            stderr=subprocess.PIPE,
                        )

                except subprocess.CalledProcessError as error:
                    print(f":: {Fore.RED}Error{Fore.RESET}:\n{error}")
                    sys.exit(1)


def main():
    # Parse arguments
    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("--output", action="store_true")
    argumentParser.add_argument("--all", action="store_true")
    arguments = argumentParser.parse_args()

    if arguments.output:
        useOutput: bool = True
    else:
        useOutput: bool = False

    if arguments.all:
        allFiles: bool = True
    else:
        allFiles: bool = False

    try:
        format(
            command=f"prettier --write --parser json",
            extension="json",
            language="JSON",
            sourcePath="../../",
            output=useOutput,
            fileAmount=allFiles,
        )
        format(
            command=f"black",
            extension="py",
            language="Python",
            sourcePath="../../",
            output=useOutput,
            fileAmount=allFiles,
        )
        format(
            command=f"uncrustify -c ../../.uncrustify.config --no-backup --replace",
            extension="java",
            language="Java",
            sourcePath="../../",
            output=useOutput,
            fileAmount=allFiles,
        )
        format(
            command=f"yamlfmt",
            extension="yml",
            language="YAML",
            sourcePath="../../",
            output=useOutput,
            fileAmount=allFiles,
        )
    except KeyboardInterrupt:  # Ignore keyboard interruption
        sys.exit()


# endregion

if __name__ == "__main__":
    main()
