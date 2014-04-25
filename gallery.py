"""
Gallery maker for scade2b.

Usage:
    gallery.py [--format=<fmt>] <testdir>...

Options:
    --format=<fmt>  Output format [default: html]

where testdirs are subdirectories of scade2b tests.
"""

import docopt
import collections
import os.path
import re
import sys
from mako.lookup import TemplateLookup
from mako.template import Template
from pygments import highlight
from pygments.lexer import RegexLexer
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter, LatexFormatter
from pygments.token import *


class ScadeLexer(RegexLexer):
    name = 'Scade'
    aliases = ['scade']
    filenames = ['*.scade']

    tokens = {
        'root': [
            (r'function', Keyword),
            (r'node', Keyword),
            (r'tel', Keyword),
            (r'let', Keyword),
            (r'var', Keyword),
            (r'returns', Keyword),
            (r'[();\[\]]', Punctuation),
            (r'[@,:^]', Operator),
            (r'\.\.', Operator),
            (r'[=+-<>]', Operator),
            (r'[<>]=', Operator),
            (r'<>', Operator),
            (r'\d+(\.\d+)?', Number),
            (r'\w+', Name),
            (r'\s+', Text),
        ]
    }


class BLexer(RegexLexer):
    name = 'B'
    aliases = ['b']
    filenames = ['*.mch', '*.imp']

    tokens = {
        'root': [
            (r'MACHINE|IMPLEMENTATION|REFINES', Keyword),
            (r'SEES|OPERATIONS|PRE|THEN|END', Keyword),
            (r'seq', Keyword),
            (r'BOOL|INT', Keyword),
            (r'<--', Operator),
            (r':=', Operator),
            (r'\|-\>', Operator),
            (r'/\|\\', Operator),
            (r'\\\|/', Operator),
            (r'[<>=]', Operator),
            (r'[-+/]', Operator),
            (r'::?', Operator),
            (r'\^', Operator),
            (r'\d+(\.\d+)?', Number),
            (r'[(){}\|,&;]', Punctuation),
            (r'\w+', Name),
            (r'\s+', Text),
        ]
    }


def category(s):
    """
    Categorize a filename.
    Returns (category, base).
    """
    if s.endswith('_i.imp'):
        base = re.sub(r'_i.imp$', '', s)
        return ('Implementation', base)
    if s.endswith('.mch'):
        base = re.sub(r'.mch$', '', s)
        return ('Abstract machine', base)
    assert False

Example = collections.namedtuple('Example', 'name scade xml b')


def ex_from_test(path):
    g = re.search(r'/(\w+)\.test', path)
    name = g.group(1)
    with open(os.path.join(path, 'KCG/kcg_xml_filter_out.scade')) as f:
        scade = f.read()
    with open(os.path.join(path, 'KCG/kcg_trace.xml')) as f:
        xml = f.read()
    b = {}
    for fn in os.listdir(os.path.join(path, 'spec')):
        (cat, base) = category(fn)
        with open(os.path.join(path, 'spec', fn)) as f:
            content = f.read()
        if base not in b:
            b[base] = {}
        b[base][cat] = content
    return Example(name, scade, xml, b)


def pyg_ex(e, formatter):
    scade_pyg = highlight(e.scade, ScadeLexer(), formatter)
    xml_pyg = highlight(e.xml, XmlLexer(), formatter)
    b_pyg = {fn:
             {k: highlight(v, BLexer(), formatter) for k, v in bfile.items()
              } for fn, bfile in e.b.items()
             }
    return Example(e.name, scade_pyg, xml_pyg, b_pyg)


def render_list(l, template_name, formatter):
    lookup = TemplateLookup(directories=['templates'])
    tpl = lookup.get_template(template_name)
    out = tpl.render(exs=[pyg_ex(e, formatter) for e in l])
    return out.encode('utf8')


def main():
    arguments = docopt.docopt(__doc__)
    test_paths = arguments['<testdir>']
    fmt = arguments['--format']
    l_ex = [ex_from_test(tp) for tp in test_paths]
    if fmt == 'html':
        if not os.path.isdir('out'):
            os.mkdir('out')
        with open('out/gallery.html', 'w') as f:
            f.write(render_list(l_ex, 'web.mako', HtmlFormatter()))
        with open('out/pygments.css', 'w') as f:
            f.write(HtmlFormatter(style='murphy').get_style_defs())
    elif fmt == 'latex':
        with open('out/gallery.tex', 'w') as f:
            f.write(render_list(l_ex, 'latex.mako', LatexFormatter()))
        with open('out/style.tex', 'w') as f:
            f.write(LatexFormatter(style='murphy').get_style_defs())
    else:
        print "Bad format: %s" % fmt
        sys.exit(1)

if __name__ == '__main__':
    main()
