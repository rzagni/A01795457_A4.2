"""
Word Frequency Counter

This script reads an ascii file, processes the words, and computes their
frequency.

It filters out invalid words (only allowing alphanumeric words and hyphenated
words). The results are displayed on the console and written to an output file.
If the output file exist, the program will append the output, otherwise a new
file will be created.

Usage:
    python word_count.py input_file

Author: Renzo Zagni
"""
import sys
import os
import time
import re

OUTPUT_FILE = "WordCountResults.txt"


def show_usage():
    """
    Prints usage instructions for the script and exits.

    Example:
        Usage: python script_name.py input_file
    """
    print(f'Usage: {os.path.basename(sys.argv[0])} input_file')
    sys.exit(1)


def is_ascii(filepath):
    """
    Checks if a file exists and is ASCII-encoded.

    Args:
        filepath (str): Path to the file.

    Returns:
        bool: True if the file is ASCII-encoded, False otherwise.
    """
    try:
        with open(filepath, 'r', encoding="ascii") as f:
            f.read().isascii()
        return True
    except FileNotFoundError:
        return False


def print_plus(content, file_handler):
    """
    Prints content to both the console and a file.

    Args:
        content (str): The text to print.
        file_handler (file object): The file to write to.
    """
    print(content)
    file_handler.write(content + "\n")


def is_valid_word(word):
    """
    Validates whether a word consists of letters, numbers, and hyphens.

    To be considered a valid word, the string must conform to the
    following rules as defined in the regular expression below

    1. A valid string must start with a letter or a digit. Tt cannot
    begin with a hyphen (-).
    2. A valid string may contain hyphens (-), but each hyphen must be
    followed by at least one letter or digit.
    3. Consecutive hyphens (--) are not allowed; each hyphen must be
    separated by alphanumeric characters.
    4. A valid string cannot end with a hyphen (-).
    5. The string must contain only letters (a-z, A-Z), digits (0-9),
    and hyphens (-)—no special characters or spaces are allowed.

    Args:
        word (str): The word to validate.

    Returns:
        bool: True if the word is valid, False otherwise.
    """
    return bool(re.fullmatch(r"[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*", word))


def main():
    """
    Main function for counting the word frequency from an input file.

    This function:
    - Reads a file specified in the command-line argument.
    - Validates that the file is ASCII-encoded.
    - Parses words from the file while filtering invalid words.
    - Counts occurrences of each valid word.
    - Outputs the results to both the console and a file.
    - Displays execution time.

    The function exits with an error message if no file is provided or if
    the file cannot be opened.
    """
    start_time = time.time()

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        show_usage()
        sys.exit(0)

    if not is_ascii(input_file):
        print(f'Unable to open input file: {input_file}')
        sys.exit(1)

    word_list = []

    with open(input_file, "r", encoding="ascii") as file:
        for _, line in enumerate(file, start=1):
            word_list.extend(line.strip().lower().split())

    word_map = {}

    for word in word_list:
        if not is_valid_word(word):
            print(f"Invalid data: {word} is not a valid word")
            continue
        if word in word_map:
            word_map[word] += 1
        else:
            word_map[word] = 1

    with open(OUTPUT_FILE, "a", encoding="ascii") as ofile:
        print_plus(f'{"Word": >26}  {"Frequency": >10}', ofile)
        print_plus(f'{"-"*26}  {"-"*10}', ofile)
        for word, frequency in word_map.items():
            print_plus(f'{word: >26}  {frequency: >10}', ofile)
        print_plus(f'Execution time: {time.time() - start_time: .5f} \
                   seconds\n', ofile)


if __name__ == "__main__":
    main()
