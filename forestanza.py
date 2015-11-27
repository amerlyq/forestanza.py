#!/usr/bin/env python3

import os
import sys

from forestanza import io
from forestanza.ftype import fb2, fza, xhtml
from forestanza.dom import ForestanzaDOM
from forestanza.syntax.vim import SynGenVim
from forestanza.source import web
from forestanza.process import google


def progress_bar(i, n):
    print("{}/{} = {}%".format(i+1, n, round(100*i/n)))


def translated(fl):
    srctxt = io.expand_pj('@/' + fl.name + '.src.txt')
    prorsp = io.expand_pj('@/' + fl.name + '.pro.rsp')

    if os.path.exists(prorsp):
        with open(prorsp, 'r') as f:
            for line in f.readlines():
                yield line
    else:
        with open(srctxt, 'r') as f:
            for line in f.readlines():
                line = gt.translate(line)
                with open(prorsp, 'a') as rsp:
                    rsp.write(line + '\n')
                yield line


class Arifureta:
    def __init__(self, chapter):
        self.url = 'http://ncode.syosetu.com/n8611bv/{:d}'.format(chapter)
        self.name = 'arifureta-{:d}'.format(chapter)

if __name__ == '__main__':
    fl = Arifureta(132)
    if len(sys.argv) > 1 and sys.argv[1] == '-r':
        io.clean_cache(fl.name)

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
    gt = google.Translator()
    lst = translated(fl)
    for i, line in enumerate(lst):
        sec = google.ResponseParser(line)
        for e in exs:
            e.p_section(i+1, sec)
        # progress_bar(i, 100)  # len(lst))

    for t, e in zip(fts, exs):
        io.export_cache(fl.name + t.EXT, lambda: e.dump())
