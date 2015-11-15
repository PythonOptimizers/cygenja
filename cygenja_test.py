from cygenja.helpers.file_helpers import find_files
from cygenja.generator import Generator
import sys
import logging



cygenja_machine = Generator('cygenja')

########################################################################################################################
logger_name = 'cygenja'
logger = logging.getLogger(logger_name)

# levels
log_level = logging.DEBUG
console_log_level = logging.DEBUG
file_log_level = logging.DEBUG

logger.setLevel(log_level)

# create console handler and set logging level
ch = logging.StreamHandler()
ch.setLevel(console_log_level)

# create file handler and set logging level
log_file_name = logger_name + '.log'
fh = logging.FileHandler(log_file_name)
fh.setLevel(file_log_level)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)

logger.info('*' * 100)
logger.info('*' * 100)
logger.info("Start some action(s)")


########################################################################################################################

print cygenja_machine.filters_list()

print cygenja_machine.registered_filters_list()

cygenja_machine.register_common_type_filters()

print cygenja_machine.registered_filters_list()

cygenja_machine.register_extension('.cpy', '.py')
cygenja_machine.register_extension('.cpx', '.pyx')

print cygenja_machine.registered_extensions_list()

print "E" * 80



def one_index():
    INDEX_LIST = ['dog', 'cat']
    context = {}
    for index in INDEX_LIST:
        context['index'] = index
        yield '_%s' % index, context


def default_index():
    INDEX_LIST = ['h', 'i', 'j']
    TYPE_LIST  = ['1', '2', '3', '4']
    context = {}
    for index in INDEX_LIST:
        context['index'] = index
        for type in TYPE_LIST:
            context['type'] = type
            yield '_%s_%s' % (index, type), context

cygenja_machine.register_action('temp/dir1/dir2', '*.cpx', one_index)
cygenja_machine.register_default_action('*', default_index)

cygenja_machine.generate('.', '*.cpx', action_ch='e', recursively=True)