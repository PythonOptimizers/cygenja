# Several helpers to find files and/or directories
import os
import fnmatch


def find_files(directory, pattern, recursively=True):
    """
    Yield a list of files with their base directories, recursively or not.

    Returns:
        A list of (base_directory, filename)

    Args:
        directory: base directory to start the search.
        pattern: fnmatch pattern for filenames.
        complete_filename: return complete filename or not?
        recursively: do we recurse or not?
    """

    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                yield root, basename
        if not recursively:
            break
