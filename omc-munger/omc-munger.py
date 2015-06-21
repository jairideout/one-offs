#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import sys
import glob
import math
import os.path

def main():
    if len(sys.argv) != 4:
        sys.exit('Usage: %s <input directory> <output filepath> <alpha>' %
                 sys.argv[0])

    input_directory, output_filepath, alpha = sys.argv[1:]

    alpha = float(alpha)
    if not 0.0 <= alpha <= 1.0:
        sys.exit('Invalid alpha: %r. Alpha must be between 0 and 1 (inclusive)'
                 % alpha)

    status('Calculating total number of tests (this may take awhile)...')
    test_count = get_test_count(input_directory)
    status('Total number of tests: %d' % test_count)

    status('Finding significant observation IDs for each category '
           '(alpha=%r)...' % alpha)
    with open(output_filepath, 'w') as output_fh:
        header = ['Category', 'Count significant',
                  'Significant observation IDs']
        output_fh.write('\t'.join(header))
        output_fh.write('\n')

        for filepath in iter_results_filepaths(input_directory):
            category, significant_ids = find_significant_correlations(
                filepath, alpha, test_count)

            if len(significant_ids) > 0:
                cells = [category, '%d' % len(significant_ids)]
                cells.append(
                    ', '.join('%s (%r, %r)' % e for e in significant_ids))

                output_fh.write('\t'.join(cells))
                output_fh.write('\n')
    status('Results are in %s' % output_filepath)


def status(msg):
    """Write message immediately to stdout."""
    sys.stdout.write(msg)
    sys.stdout.write('\n')
    sys.stdout.flush()


def get_test_count(input_directory):
    test_count = 0
    for filepath in iter_results_filepaths(input_directory):
        with open(filepath, 'U') as fh:
            # skip the header line
            next(fh)
            for line in fh:
                test_count += 1
    return test_count


def iter_results_filepaths(input_directory):
    return glob.glob(os.path.join(input_directory, 'corr_*.txt'))


def find_significant_correlations(results_filepath, alpha, test_count):
    category = os.path.splitext(results_filepath)[0].split('corr_')[1]

    with open(results_filepath, 'U') as fh:
        header = next(fh).split('\t')
        id_idx = header.index('Feature ID')
        test_stat_idx = header.index('Test stat.')
        p_value_idx = header.index('pval')

        significant_ids = []
        for line in fh:
            cells = line.split('\t')
            id_ = cells[id_idx]
            test_stat = float(cells[test_stat_idx])

            # bonferroni-correct p-value for total number of comparisons, cap
            # at 1.0. if NaN the output will still be NaN
            p_value = min(float(cells[p_value_idx]) * test_count, 1.0)

            # NaN will never be <= alpha
            if p_value <= alpha:
                significant_ids.append((id_, test_stat, p_value))
            else:
                # file is sorted by increasing p-values so we can stop
                # searching. NaNs always appear at the bottom of the file so we
                # can stop searching in that case too
                break
    return category, significant_ids


if __name__ == "__main__":
    main()
