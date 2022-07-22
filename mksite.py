#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="create a static site")
    parser.add_argument(
        "paths",
        help="path to a file to include",
        metavar="PATH",
        action="append",
        nargs="+",
        type=Path,
    )
    parser.add_argument(
        "--filter",
        help="""a filter applied to files with extension IN.
CMD will be invoked for each file, with file contents passed to stdin.
Output is read from stdout and should have extension OUT.
Filters get applied to matching files in the order they are specified""",
        nargs=3,
        metavar=("IN", "OUT", "CMD"),
        action="append",
        default=[],
    )
    args = parser.parse_args()
    print(args)


class UserError(Exception):
    pass


def normalizePath(cwd, path):
    """
    Get a normalized path, relative to the current working directory.

    An absolute path is made relative

    >>> normalizePath(Path("/root"), Path("/root/dir/file.txt")).as_posix()
    'dir/file.txt'

    A relative path is returned unchanged

    >>> normalizePath(Path("/root"), Path("dir/file.txt")).as_posix()
    'dir/file.txt'

    An error is raised when an absolute path is not under the root path

    >>> normalizePath(Path("/root"), Path("/some/file.txt")).as_posix()
    Traceback (most recent call last):
    ...
    mksite.UserError: Source file not in working directory: /some/file.txt

    """

    abs_path = path
    if not path.is_absolute():
        abs_path = cwd.joinpath(path)
    try:
        return abs_path.relative_to(cwd)
    except ValueError:
        raise UserError(f"Source file not in working directory: {path}")


if __name__ == "__main__":
    main()
