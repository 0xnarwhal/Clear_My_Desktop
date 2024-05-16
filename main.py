# -*- coding: utf-8 -*-
# main.py

"""An automation script to delete files from your directory with additional options."""
import os
from os import listdir, getcwd
from os.path import isfile, join, isdir, relpath

__author__ = "0xnarwhal"
__copyright__ = "Copyright 2024, 0xnarwhal"
__credits__ = ["0xnarwhal"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "0xnarwhal"
__email__ = "amiradrian@protonmail.com"
__status__ = "Development"

def gather_files(filter: str = None, recursive: bool = False, path: str = None) -> list:
    """
    This function gathers a list of files based on specified criteria.

    Parameters:
    - filter (str): A comma-separated list of file extensions to filter.
    - recursive (bool): Whether to search for files recursively in subdirectories.
    - path (str): The directory path to search for files.

    Returns:
    - list: A list of files that meet the specified criteria.
    """
    full_path = getcwd() if path == None else getcwd() + "/" + path

    if not isdir(full_path):
        raise ValueError("The specified path is not a valid directory.")

    files = []

    if not recursive:
        files = [f for f in listdir(full_path) if isfile(join(full_path, f))]
        if filter:
            ignore_extensions = [ext.strip() for ext in filter.split(',')]
            files = [f for f in files if not any(f.endswith(ext) for ext in ignore_extensions)]
    else:
        for root, dirs, files in os.walk(full_path):
            for file in files:
                file_path = os.path.join(root, file)
                if filter:
                    ignore_extensions = [ext.strip() for ext in filter.split(',')]
                    if not any(file_path.endswith(ext) for ext in ignore_extensions):
                        files.append(file_path)
                else:
                    files.append(file_path)

    return files

if __name__ == "__main__":
    pass