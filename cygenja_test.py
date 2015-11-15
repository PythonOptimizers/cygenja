from cygenja.helpers.file_helpers import find_files
from cygenja.generator import Generator
import sys


for filename in find_files(sys.argv[1], '*.py'):
    print filename

cygenja_machine = Generator('cygenja')

print cygenja_machine.filters_list()

print cygenja_machine.registered_filters_list()

cygenja_machine.register_common_type_filters()

print cygenja_machine.registered_filters_list()

cygenja_machine.register_extension('cpy', 'py')
cygenja_machine.register_extension('cpx', 'pyx')

print cygenja_machine.registered_extensions_list()

print "E" * 80

template_filename = '/home/nikolaj/Documents/WORK/Dominique/PROJECT/DECOUPLED_VERSION/SOLID/cygenja/template.cpx'
context = {'stranger' : 'God'}
cygenja_machine.generate_file(template_filename, context, '_taboule.txt')

cygenja_machine.generate('.', '*', 'g', False)

print "2" * 80

from cygenja.treemap.treemap import TreeMap

d = TreeMap()

d.add_element('dir1/dir2/dir3/dir4', 12)
d.add_element('dir1', 4)

d.add_element('dir22', 78)

print d.to_string()

print d.retrieve_element('dir1')