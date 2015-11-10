#!/usr/bin/env python3

import os
import sys

import forestanza
from forestanza.ftype import fb2, fza, xhtml
from forestanza import io
from forestanza.dom import ForestanzaDOM
from forestanza.syntax.vim import SynGenVim
from forestanza.source import web
from forestanza.process import google


class FileBundle:
    TMPDIR = os.getenv('TMPDIR') or os.path.join('/tmp', os.getenv('USER'))
    DSTDIR = os.path.join(TMPDIR, forestanza.__appname__)
    EXTENSIONS = ['html', 'src', 'fza', 'fb2', 'xhtml', 'xml', 'req', 'rsp']

    def __init__(self, src, name, chapter):
        self.url = src.format(chapter)
        self.name = name.format(chapter)
        self.make_paths()

    def make_paths(self):
        if not os.path.exists(FileBundle.DSTDIR):
            os.makedirs(FileBundle.DSTDIR)
        dstbase = os.path.join(FileBundle.DSTDIR, self.name)
        for ext in FileBundle.EXTENSIONS:
            setattr(self, ext, dstbase + '.' + ext)


def progress_bar(i, n):
    print("{}/{} = {}%".format(i+1, n, round(100*i/n)))


if __name__ == '__main__':
    fl = FileBundle('http://ncode.syosetu.com/n8611bv/{:d}',
                    'arifureta-{:d}', 131)

    # Clean cache and all results
    if len(sys.argv) > 1 and sys.argv[1] == '-r':
        for ext in fl.EXTENSIONS:
            if os.path.isfile(getattr(fl, ext)):
                os.remove(getattr(fl, ext))

    # NOTE: save_data() expanded to process get_page/extract only if no cache
    if not os.path.exists(fl.html):
        with open(fl.html, 'w') as f:
            f.write(web.load(fl.url))

    if not os.path.exists(fl.src):
        with open(fl.src, 'w') as f:
            f.write(os.linesep.join(web.refine(fl.html)))

    gt = google.Translator()
    bCachedRsp = os.path.exists(fl.rsp)
    with open(getattr(fl, 'rsp' if bCachedRsp else 'src'), 'r') as src:
        lst = src.readlines()

    dom = ForestanzaDOM(io.import_yaml('colorscheme'),
                        io.import_yaml('lexems-' + 'jap'))
    for k, v in SynGenVim(dom).ddump().items():
        io.export_cache(k + '.vim', v)

    efb2 = fb2.Exporter(author='Xz', title=fl.name)
    efza = fza.Exporter(author='Xz', title=fl.name)
    exhtml = xhtml.Exporter(author='Xz', title=fl.name)

    # Write main body
    with open(fl.fza, 'w') as fza:
        for i, line in enumerate(lst):
            if not bCachedRsp:
                line = gt.translate(line)
                with open(fl.rsp, 'a') as rsp:
                    rsp.write(line + '\n')

            sec = google.ResponseParser(line)
            efb2.p_section(i+1, sec)
            efza.p_section(i+1, sec)
            exhtml.p_section(i+1, sec)
            # progress_bar(i, len(lst))

    # Cover fb2 in header/footer
    with open(fl.fb2, 'w') as f:
        f.write(efb2.dump())
    with open(fl.fza, 'w') as f:
        f.write(efza.dump())
    with open(fl.xhtml, 'w') as f:
        f.write(exhtml.dump())
