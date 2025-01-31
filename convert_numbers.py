"""
Convert Numbers Script

This script reads decimal numbers from an input file and converts them
to binary and hexadecimal formats, writing the results to an output file.
If the output file exist, the program will append the output, otherwise
a new file will be created.

Usage:
    python convert_numbers.py input_file

Author: Renzo Zagni
"""

import sys
import os
import time
import math

start_time = time.time()

OUTPUT_FILE = "ConvertionResults.txt"


def show_usage():
    """
    Print usage instructions for the script and exit.

    Example:
        Usage: python script_name.py input_file
    """
    print(f'Usage: {os.path.basename(sys.argv[0])} input_file')
    sys.exit(1)


def is_ascii(filepath):
    """
    Check if a file exists and is ASCII-encoded.

    Args:
        filepath (str): Path to the file.

    Returns:
        bool: True if the file is ASCII-encoded and exists,
              False otherwise.
    """
    try:
        with open(filepath, 'r', encoding="ascii") as f:
            return f.read().isascii()
    except FileNotFoundError:
        return False


def decimal_to_binary(decimal_number):
    """
    Convert a decimal number to its binary representation.

    Args:
        decimal_number (float or int): The number to convert.

    Returns:
        str: Binary representation of the number.
    """
    if decimal_number == 0:
        return "0"

    is_negative = decimal_number < 0
    decimal_number = abs(decimal_number)
    integer_number = int(decimal_number)
    fractional_number = decimal_number - integer_number

    binary_integer = ""
    while integer_number > 0:
        remainder = integer_number % 2
        binary_integer = str(remainder) + binary_integer
        integer_number //= 2

    binary_integer = binary_integer or "0"

    binary_fraction = ""
    while fractional_number > 0 and len(binary_fraction) < 10:
        fractional_number *= 2
        bit = int(fractional_number)
        binary_fraction += str(bit)
        fractional_number -= bit

    binary_number = binary_integer
    if binary_fraction:
        binary_number += "." + binary_fraction

    return f'-{binary_number}' if is_negative else binary_number


def decimal_to_hexa(decimal_number):
    """
    Convert a decimal number to its hexadecimal representation.

    Args:
        decimal_number (float or int): The number to convert.

    Returns:
        str: Hexadecimal representation of the number.
    """
    if decimal_number == 0:
        return "0"

    is_negative = decimal_number < 0
    decimal_number = abs(decimal_number)
    integer_number = int(decimal_number)
    fractional_number = decimal_number - integer_number

    hexadecimal_digits = "0123456789ABCDEF"

    hexadecimal_integer = ""
    while integer_number > 0:
        remainder = integer_number % 16
        hexadecimal_integer = (
            hexadecimal_digits[remainder] + hexadecimal_integer
        )
        integer_number //= 16

    hexadecimal_integer = hexadecimal_integer or "0"

    hexadecimal_fraction = ""
    while fractional_number > 0 and len(hexadecimal_fraction) < 10:
        fractional_number *= 16
        digit = int(fractional_number)
        hexadecimal_fraction += hexadecimal_digits[digit]
        fractional_number -= digit

    hexadecimal_number = hexadecimal_integer
    if hexadecimal_fraction:
        hexadecimal_number += "." + hexadecimal_fraction

    return f'-{hexadecimal_number}' if is_negative else hexadecimal_number


def print_plus(content, file_handler):
    """
    Print content to both the console and a file.

    Args:
        content (str): The text to print.
        file_handler (file object): The file to write to.
    """
    print(content)
    file_handler.write(content + "\n")


def main():
    """
    Read numbers from an input file, convert them to binary and
    hexadecimal formats, and save the results to an output file.
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
                if input_number.is_integer():
                    input_number = int(input_number)
                valid_numbers.append(input_number)
            except ValueError:
                print(f"Line {line_number} is not a valid number: {line}")
                continue

    with open(OUTPUT_FILE, "a", encoding="ascii") as ofile:
        print_plus(
            f'{"Decimal":>15}  {"Binary":>30}  {"Hexadecimal":>12}', ofile
        )
        print_plus(f'{"-"*15}  {"-"*30}  {"-"*12}', ofile)
        for number in valid_numbers:
            decimal_str = (
                f"{number:,.6f}" if isinstance(number, float)
                else f"{number:,}"
            )
            binary_str = decimal_to_binary(number).rjust(30)
            hex_str = decimal_to_hexa(number).rjust(12)
            print_plus(f'{decimal_str:>15}  {binary_str}  {hex_str}', ofile)


if __name__ == "__main__":
    main()
