"""
Compute Statistics Script

This script reads numerical data from an input file, computes statistical
measures (mean, median, mode, variance, and standard deviation), and writes
the results to an output file. If the output file exist, the program will
append the output, otherwise a new file will be created.

Usage:
    python compute_statistics.py input_file
"""

import sys
import os
import time
import math

start_time = time.time()

OUTPUT_FILE = "StatisticsResults.txt"


def show_usage():
    """
    Prints usage instructions for the script and exits.

    Example:
        Usage: python compute_statistics.py input_file
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


def get_mean(numbers):
    """
    Calculates the mean of a list of numbers.

    Args:
        numbers (list): A list of numeric values.

    Returns:
        float: The mean of the numbers.
    """
    return sum(numbers) / len(numbers)


def get_median(numbers):
    """
    Calculates the median of a list of numbers.

    Args:
        numbers (list): A list of numeric values.

    Returns:
        float: The median of the numbers.
    """
    sorted_numbers = sorted(numbers)
    numbers_len = len(numbers)
    if numbers_len % 2 == 0:
        mid1 = sorted_numbers[numbers_len // 2 - 1]
        mid2 = sorted_numbers[numbers_len // 2]
        return (mid1 + mid2) / 2
    return sorted_numbers[numbers_len // 2]


def get_mode(numbers):
    """
    Calculates the mode(s) of a list of numbers.

    Args:
        numbers (list): A list of numeric values.

    Returns:
        list: A list of modes (most frequently occurring numbers).
    """
    frequency = {}
    modes = []
    for number_index in numbers:
        frequency[number_index] = frequency.get(number_index, 0) + 1
    max_count = max(frequency.values())
    for number_index, count in frequency.items():
        if count == max_count:
            modes.append(number_index)
    return modes


def get_variance(numbers):
    """
    Calculates the variance of a list of numbers.

    Args:
        numbers (list): A list of numeric values.

    Returns:
        float: The variance of the numbers.
    """
    local_mean = get_mean(numbers)
    variance_sum = sum((x - local_mean) ** 2 for x in numbers)
    return variance_sum / len(numbers)


def get_std_dev(variance_var):
    """
    Calculates the standard deviation from the variance.

    Args:
        variance (float): The variance of a list of numbers.

    Returns:
        float: The standard deviation.
    """
    return variance_var ** 0.5


def print_plus(content, file_handler):
    """
    Prints content to both the console and a file.

    Args:
        content (str): The text to print.
        file_handler (file object): The file to write to.
    """
    print(content)
    file_handler.write(content + "\n")


def main():
    """
    Read numbers from an input file, compute descriptive statistics,
    and save the results to an output file.
    """
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        show_usage()
        sys.exit(0)

    if not is_ascii(input_file):
        print(f'Unable to open input file: {input_file}')
        sys.exit(1)

    valid_numbers = []

    with open(input_file, "r", encoding="ascii") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            try:
                input_number = float(line)
                if math.isnan(input_number):
                    raise ValueError
                if input_number in (float('inf'), float('-inf')):
                    raise ValueError
                valid_numbers.append(input_number)
            except ValueError:
                print(f"Line {line_number} is not a valid number: {line}")

    if len(valid_numbers) == 0:
        print("Error: No valid numbers found in the input file.")
        sys.exit(1)

    if len(valid_numbers) == 1:
        print("Only one number provided. Variance and standard deviation \
              cannot be calculated.")
        sys.exit(1)

    mean = get_mean(valid_numbers)
    median = get_median(valid_numbers)
    mode = get_mode(valid_numbers)
    variance = get_variance(valid_numbers)
    standard_deviation = get_std_dev(variance)

    end_time = time.time()
    execution_time = end_time - start_time

    with open(OUTPUT_FILE, "a", encoding="ascii") as ofile:
        print_plus(f'Mean: {mean}', ofile)
        print_plus(f'Median: {median}', ofile)
        print_plus(f'Mode: {mode}', ofile)
        print_plus(f'Variance: {variance}', ofile)
        print_plus(f'Standard Deviation: {standard_deviation}', ofile)
        print_plus(f'Execution time: {execution_time:.5f} seconds\n', ofile)


if __name__ == "__main__":
    main()
