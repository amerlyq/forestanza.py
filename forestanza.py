#!/usr/bin/env python3

import os
import time

from forestanza import io
from forestanza.opts import make_options
from forestanza.ftype import fb2, fza, xhtml
from forestanza.dom import ForestanzaDOM
from forestanza.syntax.vim import SynGenVim
from forestanza.syntax.xhtml import SynGenXHTML
from forestanza.source import web
from forestanza.process import google


def progress_bar(i, n):
    print("{}/{} = {}%".format(i+1, n, round(100*i/n)))


def translated(gt, fl):
    srctxt = io.expand_pj('@/' + fl.name + '.src.txt')
    prorsp = io.expand_pj('@/' + fl.name + '.pro.rsp')

    if os.path.exists(srctxt):
        with open(srctxt, 'r') as f:
            fl.N = sum(1 for L in f)

    # WARNING: manually deleting lines in 'prorsp' allowed only from the end
    if os.path.exists(prorsp):
        with open(prorsp, 'r') as f:
            lst = f.readlines()
            proN = len(lst)
            if not hasattr(fl, 'N') or not fl.N:
                fl.N = proN
            for line in lst:
                yield line

    # ATTENTION: Will die if srctxt is non-existent/corrupted
    with open(srctxt, 'r') as f:
        lst = f.readlines()
        # Process only not cached part
        if 'proN' in locals():
            lst = lst[proN:]
        for line in lst:
            line = gt.translate(line)
            with open(prorsp, 'a') as rsp:
                rsp.write(line + '\n')
            yield line


class Chapter:
    def __init__(self, args, chapter):
        self.url = args.url.format(chapter)
        self.name = args.name.format(chapter)
        self.basepath = io.expand_pj('@/' + self.name)


def main(dom, fl):
    src = fl.name + '.src.html'
    io.export_cache(src, lambda: web.load(fl.url), keep=True)
    io.export_cache(fl.name + '.src.txt',
                    lambda: web.refine(io.expand_pj('@/' + src)), keep=True)

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


def res(dom):
    print('> color-syntax.css')
    io.export_cache('fza/color-syntax.css', SynGenXHTML(dom).colors())

    print('> *.css')
    fnm = io.expand_pj([':', 'forestanza', 'ftype', 'xhtml.css'])
    with open(fnm) as f:
        io.export_cache('fza/color-theme-wood.css', f.read())

    print('> *.js')
    fnm = io.expand_pj([':', 'forestanza', 'ftype', 'xhtml.js'])
    with open(fnm) as f:
        io.export_cache('fza/scrollPos.js', f.read())


if __name__ == '__main__':
    tbeg_whole = time.time()
    args = make_options().parse_args()
    io.DSTDIR = args.outdir

    print(">>> Forestanza <<<")
    dom = ForestanzaDOM(io.import_yaml('colorscheme'),
                        io.import_yaml('lexems-' + 'jap'))
    res(dom)
    if args.vimsyntax:
        for k, v in SynGenVim(dom).ddump():
            print('> {}.vim'.format(k))
            io.export_cache(k + '.vim', v)

    for i in args.chapters:
        tbeg_chap = time.time()
        fl = Chapter(args, i)
        if args.remove:
            io.clean_cache(fl.name)
        print("\n--- {} ---".format(fl.name))
        main(dom, fl)
        print("= {} s  > {}.*".format(time.time() - tbeg_chap,
                                      fl.basepath.replace(os.environ['HOME'], '~')))

    print("\n=== {} s // Total".format(time.time() - tbeg_whole))
