"""
Gallery maker for scade2b.

Usage : python gallery.py /path/to/name.test ...

where name.test is a subdirectory of scade2b tests.

It will output a html gallery to out/gallery.html.
"""

import os.path
import re
import sys
from mako.lookup import TemplateLookup
from mako.template import Template
from pygments import highlight
from pygments.lexer import RegexLexer
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter
from pygments.token import *


class ScadeLexer(RegexLexer):
    name = 'Scade'
    aliases = ['scade']
    filenames = ['*.scade']

    tokens = {
        'root': [
            (r'function', Keyword),
            (r'tel', Keyword),
            (r'let', Keyword),
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
            (r'MACHINE|IMPLEMENTATION|REFINES|SEES|OPERATIONS|END', Keyword),
            (r'seq', Keyword),
            (r'BOOL', Keyword),
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


def highlight_b(s):
    """
    Highlight a string of B code
    """
    return highlight(s, BLexer(), HtmlFormatter())


class Example(object):

    def __init__(self, name, scade, xml, b):
        self.name = name
        self.scade = scade
        self.xml = xml
        self.b = b

    @staticmethod
    def from_test(path):
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

    @staticmethod
    def render_list(l):

        def pyg_ex(e):
            scade_pyg = highlight(e.scade, ScadeLexer(), HtmlFormatter())
            xml_pyg = highlight(e.xml, XmlLexer(), HtmlFormatter())
            b_pyg = {fn:
                     {k: highlight_b(v) for k, v in bfile.items()
                      } for fn, bfile in e.b.items()
                     }
            return {'scade': scade_pyg,
                    'xml': xml_pyg,
                    'b': b_pyg,
                    'name': e.name,
                    }

        lookup = TemplateLookup(directories=['templates'], default_filters=['h'])
        tpl = lookup.get_template('gallery.mako')
        out = tpl.render(exs=[pyg_ex(e) for e in l])
        return out.encode('utf8')




def main():
    if len(sys.argv) <= 1:
        print __doc__
        sys.exit(1)
    test_paths = sys.argv[1:]
    l_ex = [Example.from_test(tp) for tp in test_paths]
    if not os.path.isdir('out'):
        os.mkdir('out')
    with open('out/gallery.html', 'w') as f:
        f.write(Example.render_list(l_ex))
    with open('out/pygments.css', 'w') as f:
        f.write(HtmlFormatter(style='murphy').get_style_defs())

if __name__ == '__main__':
    main()
