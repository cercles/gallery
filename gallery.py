import os.path
import sys
from mako.template import Template
from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter


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
        b = "B"
        return Example(scade, xml, b)

    def render(self):
        tpl_file = 'templates/gallery.mako'
        tpl = Template(filename=tpl_file, default_filters=['h'])
        xml_pyg = highlight(self.xml, XmlLexer(), HtmlFormatter())
        out = tpl.render(scade=self.scade, xml=xml_pyg, b=self.b)
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
