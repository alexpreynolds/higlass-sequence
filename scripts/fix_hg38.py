#!/usr/bin/env python

import sys

cs_fn = sys.argv[1]
fa_in_fn = sys.argv[2]
fa_out_fn = sys.argv[3]

cs = {}
with open(cs_fn, 'r') as cs_fh:
    for line in cs_fh:
        (chrom, size) = line.rstrip().split('\t')
        cs[chrom] = int(size)

line_idx = 0
chrom_current = None
chrom_current_size = None
chrom_desired_size = None
skip_chrom = True
with open(fa_in_fn, 'r') as fa_in_fh, open(fa_out_fn, 'w') as fa_out_fh:
    for line in fa_in_fh:
        line = line.rstrip()
        if line.startswith('>'): # header
            if chrom_current and not skip_chrom: # write out remaining bases
                sys.stderr.write('writing to {}: {}-{} = {}\n'.format(chrom_current, chrom_desired_size, chrom_current_size, chrom_desired_size - chrom_current_size))
                remaining_bases = ['N'] * (chrom_desired_size - chrom_current_size)
                fa_out_fh.write('{}\n'.format(''.join(remaining_bases)))
            chrom_current = line.lstrip('>')
            chrom_current_size = 0
            try:
                chrom_desired_size = cs[chrom_current]
                skip_chrom = False
            except KeyError:
                skip_chrom = True
        else: # sequence
            if not skip_chrom:
                chrom_current_size += len(line)
        if not skip_chrom:
            fa_out_fh.write('{}\n'.format(line))
        line_idx += 1
    # last bit
    if not skip_chrom:
        remaining_bases = ['N'] * (chrom_desired_size - chrom_current_size)
        fa_out_fh.write('{}\n'.format(''.join(remaining_bases)))
