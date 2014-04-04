import os.path
import sys
from mako.template import Template


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
        out = tpl.render(scade=self.scade, xml=self.xml, b=self.b)
        return out.encode('utf8')


def main():
    test_path = sys.argv[1]
    e = Example.from_test(test_path)
    print e.render()

if __name__ == '__main__':
    main()
