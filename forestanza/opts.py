from argparse import ArgumentParser

import forestanza
from forestanza import io


def make_options():
    parser = ArgumentParser(prog=forestanza.__appname__,
                            description='dld + tr')
    opt = parser.add_argument

    opt('chapters', metavar='C', type=int, nargs='*', default=[],
        help='an integer list of chapters for the target')

    opt('-o', '--outdir', type=str, default=io.DSTDIR,
        help='output dir for chapters and cache files')
    opt('-r', '--remove', action='store_true', default=None,
        help='remove cached files for this chapter number')
    opt('-v', '--vimsyntax', action='store_true', default=None,
        help='vim syntax files to highlight *.fza format')

    opt('-u', '--url', type=str,
        default='http://ncode.syosetu.com/n8611bv/{:d}',
        help='direct url or its template with {:d} specifier')
    opt('-n', '--name', type=str,
        default='arifureta-{:d}',
        help='name template for generated chapters')
    return parser
