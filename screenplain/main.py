#!/usr/bin/env python

# Copyright (c) 2011 Martin Vilcans
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license.php

import fileinput
import sys
import codecs
from optparse import OptionParser

from screenplain.parsers.spmd import parse

output_formats = (
    'text', 'pdf', 'fdx', 'html'
)

usage = 'Usage: %prog [options] input-file output-file'


def main(args):
    parser = OptionParser(usage=usage)
    parser.add_option(
        '-f', '--format', dest='output_format',
        metavar='FORMAT',
        help=('Set what kind of file to create. FORMAT can be any of '
            + ', '.join(output_formats))
    )
    parser.add_option(
        '--bare',
        action='store_true',
        dest='bare',
        help=(
            'For HTML output, only output the actual screenplay, '
            'not a complete HTML document.'
        )
    )
    options, args = parser.parse_args(args)
    if len(args) != 2:
        parser.error('Expected input-file and output-file arguments')
    input_file, output_file = args

    if options.output_format == None:
        if output_file.endswith('.pdf'):
            options.output_format = 'pdf'
        elif output_file.endswith('.fdx'):
            options.output_format = 'fdx'
        elif output_file.endswith('.html'):
            options.output_format = 'html'
        else:
            options.output_format = 'text'

    if options.output_format not in output_formats:
        parser.error(
            'Unknown output format. Expected one of: ' +
            ', '.join(output_formats))

    input = codecs.open(input_file, 'r', 'utf-8')
    screenplay = parse(input)

    if options.output_format == 'pdf':
        from screenplain.export.pdf import to_pdf
        to_pdf(screenplay, output_file)
    else:
        output = codecs.open(output_file, 'w', 'utf-8')
        try:
            if options.output_format == 'text':
                from screenplain.export.text import to_text
                to_text(screenplay, output)
            elif options.output_format == 'fdx':
                from screenplain.export.fdx import to_fdx
                to_fdx(screenplay, output)
            elif options.output_format == 'html':
                from screenplain.export.html import convert
                convert(screenplay, output, bare=options.bare)
        finally:
            output.close()

if __name__ == '__main__':
    main(sys.argv[1:])
