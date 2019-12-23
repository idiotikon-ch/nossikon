#!/usr/bin/env python3

import argparse
import sys
import csv


NULL_CHAR = '\u0000'
OUT_SUFFIX = '.mapped'


def _get_char(decimal_str):
    if decimal_str == 'del':
        return ''
    if decimal_str == 'null':
        return '\u0000'
    try:
        char = chr(int(decimal_str))
    except ValueError:
        raise RuntimeError('{} is not a valid codepoint'.format(decimal_str))
    return char


def read_maptable(file):
    mappings = {}
    reader = csv.reader(file, delimiter='\t')
    for cp_orig, *cps_nossikon in reader:
        try:
            char_orig = _get_char(cp_orig)
            chars_nossikon = [_get_char(cp) for cp in cps_nossikon if cp]
        except Exception as e:
            raise RuntimeError('{}: {}'.format(file.name, e))
        if len(cps_nossikon) == 0:
            raise RuntimeError(
                '{}: {} is not mapped to anything'.format(file.name, cp_orig))
        mappings[char_orig] = ''.join(chars_nossikon)
    return mappings


def parse_args():
    parser = argparse.ArgumentParser(
        description='script for mapping characters to Nossikon')
    parser.add_argument(
        'maptable', type=open,
        help='path to TSV mapping table')
    parser.add_argument(
        'files', metavar='file', type=open, nargs='*', default=[sys.stdin],
        help='text file to be mapped (default: standard input)')
    parser.add_argument(
        '--to-files', '-o', dest='to_files', action='store_true',
        help='write output to files with the suffix "{}" '
             '(otherwise write to standard output)'.format(OUT_SUFFIX))
    return parser.parse_args()


def main(args):
    mappings = read_maptable(args.maptable)
    outfile = sys.stdout
    for file in args.files:
        if args.to_files:
            outfile = open(file.name + OUT_SUFFIX, 'w')
        for line in file:
            mapped_line = ''
            for char in line:
                if char in mappings:
                    mapped_line += mappings[char]
                else:
                    mapped_line += char
            outfile.write(mapped_line)


if __name__ == '__main__':
    args = parse_args()
    main(args)
