import os
from os import listdir, getcwd
from os.path import isfile, join, isdir
import re
import argparse

__author__ = "0xnarwhal"
__copyright__ = "Copyright 2024, 0xnarwhal"
__credits__ = ["0xnarwhal"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "0xnarwhal"
__email__ = "amiradrian@protonmail.com"
__status__ = "Development"

def load_ignore_config(path: str) -> list:
    """
    This function loads the ignore configuration file and returns a list of patterns to ignore.

    Parameters:
    - path (str): The path to the ignore configuration file.

    Returns:
    - list: A list of patterns to ignore.
    """
    with open(path, 'r') as f:
        out = [re.compile(line.strip()) for line in f.readlines()]
        return out

def gather_files(filter: str = None, recursive: int = 0, path: str = None) -> list:
    """
    This function gathers a list of files based on specified criteria.

    Parameters:
    - filter (str): A comma-separated list of file extensions to filter.
    - recursive (int): The number of levels of directories to search for files.
    - path (str): The directory path to search for files.

    Returns:
    - list: A list of files that meet the specified criteria.
    """
    full_path = getcwd() if path == None else getcwd() + "/" + path

    if not isdir(full_path):
        raise ValueError("The specified path is not a valid directory.")
    files = []
    def walk_directory(root, depth, filter=None):
        nonlocal files
        ignore_patterns = load_ignore_config('ignore.cfg')
        for file in listdir(root):
            file_path = join(root, file)
            if isfile(file_path) or isdir(file_path):
                if not filter or not any(file_path.endswith(ext) for ext in filter):
                    if not any(pattern.search(file_path) for pattern in ignore_patterns):
                        files.append(file_path)
            elif depth > 0 and isdir(file_path):
                if not any(re.match(pattern.pattern, file) for pattern in ignore_patterns):
                    walk_directory(file_path, depth - 1, filter)
    walk_directory(full_path, recursive, filter)

    return files

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filter", help="Comma-separated list of file extensions to filter.")
    parser.add_argument("-r", "--recursive", type=int, help="The number of levels of directories to search for files.")
    parser.add_argument("-p", "--path", help="The directory path to search for files.")
    
    args = parser.parse_args()
    print(gather_files(args.filter, args.recursive, args.path))
