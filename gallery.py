import os.path
import sys
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
            (r'[@,:^=]', Operator),
            (r'\.\.', Operator),
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
            (r'=', Operator),
            (r'\+', Operator),
            (r'::?', Operator),
            (r'\^', Operator),
            (r'\d+(\.\d+)?', Number),
            (r'[(){}\|,&]', Punctuation),
            (r'\w+', Name),
            (r'\s+', Text),
        ]
    }


class Example(object):

    def __init__(self, scade, xml, b):
        self.scade = scade
        self.xml = xml
        self.b = b

    @staticmethod
    def from_test(path):
        with open(os.path.join(path, 'KCG/kcg_xml_filter_out.scade')) as f:
            scade = f.read()
        with open(os.path.join(path, 'KCG/kcg_trace.xml')) as f:
            xml = f.read()
        b = {}
        for fn in os.listdir(os.path.join(path, 'spec')):
            (base, ext) = os.path.splitext(fn)
            with open(os.path.join(path, 'spec', fn)) as f:
                content = f.read()
            if base not in b:
                b[base] = {}
            b[base][ext] = content
        return Example(scade, xml, b)

    def render(self):
        tpl_file = 'templates/gallery.mako'
        tpl = Template(filename=tpl_file, default_filters=['h'])
        scade_pyg = highlight(self.scade, ScadeLexer(), HtmlFormatter())
        xml_pyg = highlight(self.xml, XmlLexer(), HtmlFormatter())
        def hl_b(s):
            return highlight(s, BLexer(), HtmlFormatter())
        b_pyg = {fn: {k: hl_b(v) for k, v in bfile.items()} for fn, bfile in self.b.items()}
        #b_pyg = {}
        #for fn, d in self.b.items():
            #print d
            #b_pyg[d] = {'.mch': hl_b(d['.mch'])}
        out = tpl.render(scade=scade_pyg, xml=xml_pyg, b=b_pyg)
        return out.encode('utf8')


def main():
    test_path = sys.argv[1]
    e = Example.from_test(test_path)
    if not os.path.isdir('out'):
        os.mkdir('out')
    with open('out/gallery.html', 'w') as f:
        f.write(e.render())
    with open('out/pygments.css', 'w') as f:
        f.write(HtmlFormatter().get_style_defs())

if __name__ == '__main__':
    main()
