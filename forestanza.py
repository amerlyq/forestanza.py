#!/usr/bin/env python3

import os
from argparse import ArgumentParser

from forestanza import io
from forestanza.ftype import fb2, fza, xhtml
from forestanza.dom import ForestanzaDOM
from forestanza.syntax.vim import SynGenVim
from forestanza.source import web
from forestanza.process import google


def progress_bar(i, n):
    print("{}/{} = {}%".format(i+1, n, round(100*i/n)))


def translated(gt, fl):
    srctxt = io.expand_pj('@/' + fl.name + '.src.txt')
    prorsp = io.expand_pj('@/' + fl.name + '.pro.rsp')

    if os.path.exists(prorsp):
        with open(prorsp, 'r') as f:
            lst = f.readlines()
            fl.N = len(lst)
            for line in lst:
                yield line
    else:
        with open(srctxt, 'r') as f:
            lst = f.readlines()
            fl.N = len(lst)
            for line in lst:
                line = gt.translate(line)
                with open(prorsp, 'a') as rsp:
                    rsp.write(line + '\n')
                yield line


class Arifureta:
    def __init__(self, chapter):
        self.url = 'http://ncode.syosetu.com/n8611bv/{:d}'.format(chapter)
        self.name = 'arifureta-{:d}'.format(chapter)


def main(fl):
    src = fl.name + '.src.html'
    io.export_cache(src, lambda: web.load(fl.url), keep=True)
    io.export_cache(fl.name + '.src.txt',
                    lambda: web.refine(io.expand_pj('@/' + src)), keep=True)

    dom = ForestanzaDOM(io.import_yaml('colorscheme'),
                        io.import_yaml('lexems-' + 'jap'))
    for k, v in SynGenVim(dom).ddump():
        io.export_cache(k + '.vim', v)

    fts = [fb2, fza, xhtml]
    exs = [t.Exporter(dom, author='Xz', title=fl.name) for t in fts]

    # Write main body
    lst = translated(google.Translator(), fl)
    for i, line in enumerate(lst):
        sec = google.ResponseParser(line)
        for e in exs:
            e.p_section(i+1, sec)
        progress_bar(i, fl.N)

    for t, e in zip(fts, exs):
        io.export_cache(fl.name + t.EXT, lambda: e.dump())


if __name__ == '__main__':
    parser = ArgumentParser(description='dld + tr')
    parser.add_argument('chapters', metavar='C', type=int, nargs='+', default=[],
                        help='an integer list for the target chapters')
    parser.add_argument('-r', '--remove', action='store_true', default=None,
                        help='')

    args = parser.parse_args()

    for i in args.chapters:
        fl = Arifureta(i)
        if args.remove:
            io.clean_cache(fl.name)
        main(fl)
