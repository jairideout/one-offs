#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import sys

import biom
import skbio.diversity


def main():
    if len(sys.argv) != 4:
        sys.exit(
            'Usage: %s <input BIOM file> <output filepath> '
            '<alpha diversity metric>\n'
            'Example: %s table.biom results.txt pielou_e' %
            (sys.argv[0], sys.argv[0]))

    biom_fp, output_fp, metric = sys.argv[1:]

    status('Loading BIOM table...')
    table = biom.load_table(biom_fp)
    sample_ids = table.ids('sample')

    status('Obtaining dense array from BIOM table (if you run out of memory, '
           'email Jai)...')
    table_data = table.transpose().matrix_data.toarray().astype(
        int, casting='unsafe')

    status('Computing alpha diversity for each sample (metric=%s)...' % metric)
    results = skbio.diversity.alpha_diversity(metric, table_data,
                                              ids=sample_ids)

    with open(output_fp, 'w') as output_fh:
        output_fh.write('\t%s\n' % metric)
        results.to_csv(output_fh, sep='\t', index=True, decimal='.',
                       na_rep='nan')
    status('Results are in %s' % output_fp)


def status(msg):
    """Write message immediately to stdout."""
    sys.stdout.write(msg)
    sys.stdout.write('\n')
    sys.stdout.flush()


if __name__ == "__main__":
    main()
