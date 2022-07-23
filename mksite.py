#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3

import argparse
from pathlib import Path
from collections import defaultdict
from subprocess import run


def main():
    parser = argparse.ArgumentParser(description="create a static site")
    parser.add_argument(
        "paths",
        help="path to a file to include",
        metavar="PATH",
        action="store",
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
    files = readFiles(args.paths)
    filteredFiles = applyFilters(files, args.filter)
    print(filteredFiles)


def readFiles(paths):
    files = []
    cwd = Path.cwd()
    for path in paths:
        if not path.exists():
            raise UserError(f"Path does not exist: {path}")
        relPath = normalizePath(cwd, path)
        contents = path.read_bytes()
        files.append({"path": relPath, "contents": contents})
    return files


def applyFilters(files, filters):
    """
    Apply all filters in order on matching files

    File contents are modified by filter

    >>> applyFilters(\
            [ {'path': Path('hi.txt'), 'contents': b'hi'} ],\
            [ ("txt", "md", "echo ho") ]\
            )
    [{'path': PosixPath('hi.md'), 'contents': b'ho\\n'}]

    Filter matches only files with the right extension

    >>> applyFilters(\
            [ {'path': Path('hi.md'), 'contents': b''}\
            , {'path': Path('style.css'), 'contents': b''}\
            ],\
            [ ("md", "html", "cat") ])
    [{'path': PosixPath('style.css'), 'contents': b''}, \
{'path': PosixPath('hi.html'), 'contents': b''}]

    Files can pass through multiple filters in sequence

    >>> applyFilters(\
            [ {'path': Path('recipe.cooklang'), 'contents': b''}\
            , {'path': Path('index.md'), 'contents': b''}\
            ],\
            [ ("cooklang", "md", "cat"), ("md", "html", "cat") ])
    [{'path': PosixPath('index.html'), 'contents': b''}, \
{'path': PosixPath('recipe.html'), 'contents': b''}]
    """

    filesByExtension = groupBy(files, lambda file: file["path"].suffix)
    for (inExt, outExt, cmd) in filters:
        for file in filesByExtension.pop(f".{inExt}"):
            file["path"] = file["path"].with_suffix(f".{outExt}")
            res = run(cmd, input=file["contents"], shell=True, capture_output=True)
            if res.returncode > 0:
                raise UserError(f"Running filter cmd {cmd} failed:\n{res.stdout}")
            file["contents"] = res.stdout
            filesByExtension[f".{outExt}"].append(file)
    return [file for filesWithExt in filesByExtension.values() for file in filesWithExt]


class UserError(Exception):
    pass


def groupBy(items, groupFn):
    """
    Group items by a value returned from grouping function

    >>> groupBy(['a', 'aa', 'b'], lambda str: len(str))
    defaultdict(<class 'list'>, {1: ['a', 'b'], 2: ['aa']})
    """

    groups = defaultdict(list)
    for item in items:
        groups[groupFn(item)].append(item)

    return groups


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
