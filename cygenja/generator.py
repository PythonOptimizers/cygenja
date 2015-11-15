from jinja2 import Environment, FileSystemLoader
import os
import glob

from cygenja.filters.type_filters import *
from cygenja.helpers.file_helpers import find_files
from cygenja.treemap.treemap import TreeMap


class GeneratorAction(object):
    def __init__(self, file_pattern, action_function):
        """
        """
        super(GeneratorAction, self).__init__()
        self.__file_pattern = file_pattern
        self.__action_function = action_function

    def run(self):
        yield self.__action_function()


class Generator(object):
    """
    Main class for :program:`cygenja`.


    """
    def __init__(self, directory, logger=None, raise_exception_on_warning=False):
        """
        Constructor of a :program:`cygenja` template machine.

        Args:
            directory (str): Absolute or relative base directory. Everything happens in that directory and sub-directories.
            logger: A logger (from the standard ``logging``) or ``None`` is no logging is wanted.
            raise_exception_on_warning (bool): If set to ``True``, raise a ``RuntimeError`` when logging a warning.
        """
        super(Generator, self).__init__()

        # before all the rest, prepare logging
        self.__logger = logger
        self.__raise_exception_on_warning = raise_exception_on_warning

        # test if directory exists
        if not os.path.isdir(directory):
            self.log_error('Main directory \'%s\' does not exists!' % directory)

        self.__directory = os.path.abspath(directory)   # main base directory
        self.__jinja2_environment = Environment(autoescape=False,
                                                loader=FileSystemLoader('/'), # we use absolute filenames
                                                trim_blocks=False,
                                                variable_start_string='@',
                                                variable_end_string='@')

        self.__jinja2_predefined_filters = self.__jinja2_environment.filters.keys()



        self.__extensions = {}
        self.__actions = TreeMap()

    ###########################################################################
    # LOGGING
    ###########################################################################
    def log_info(self, msg):
        """
        Log an information message if ``logger`` exists.

        Args:
            msg: Message to log.

        """
        if self.__logger:
            self.__logger.info(msg)

    def log_warning(self, msg):
        """
        Log a warning if ``logger`` exists.

        Args:
            msg: Warning to log.

        Warning:
            Can raise a ``RuntimeError`` if this was asked in the constructor.

        """
        if self.__logger:
            self.__logger.warning(msg)

        if self.__raise_exception_on_warning:
            raise RuntimeError(msg)

    def log_error(self, msg):
        """
        Log an error and raise an exception.

        Args:
            msg: Error message to log.

        Raises:
            RuntimeError: With the message.
        """
        if self.__logger:
            self.__logger.error(msg)

        raise RuntimeError(msg)

    ###########################################################################
    # FILTERS
    ###########################################################################
    def register_filter(self, filter_name, filter_ref, force=False):
        """
        Add/register one filter.

        Args:
            filter_name (str): Filter name used inside :program:`Jinja2` tags.
            filter_ref: Reference to the filter itself, i.e. the corresponding :program:`Python` function.
            force (bool): If set to ``True``, forces the registration of a filter no matter if it already exists or not.

        Note:
            The list of user added/registered filters can be retrieve with :mth:`registered_filters_list`
        """
        if not force and (filter_name in self.filters_list()):
            self.log_warning("Extension %s already exist, ignore redefinition." % ext_in)
            return

        self.__jinja2_environment.filters[filter_name] = filter_ref

    def register_filters(self, filters, force=False):
        """
        Add/register filters.

        Args:
            filters (dict): Dictionary of Python functions to use as :program:`Jinja2` filters.
            force (bool): If set to ``True``, forces the registration of a filter no matter if it already exists or not.

        """
        for filter_name, filter_ref in filters.items():
            self.register_filter(filter_name, filter_ref, force)

    def filters_list(self):
        """
        Return the list of **all** filters (as a list of strings).

        The list includes predefined :program:`Jinja2` filters.


        """
        return self.__jinja2_environment.filters.keys()

    def registered_filters_list(self):
        """
        Return the list of registered filters (as a list of strings).

        The list **only** includes registered filters (**not** the predefined :program:`Jinja2` filters).

        """
        return [filter_name for filter_name in self.__jinja2_environment.filters.keys() if filter_name not in self.__jinja2_predefined_filters ]

    # TODO: out of here!
    def register_common_type_filters(self):
        """
        Add/register common type filters for the :program:`CySparse` project.

        """
        self.register_filter('type2enum', type2enum)
        self.register_filter('cysparse_type_to_numpy_c_type', cysparse_type_to_numpy_c_type)
        self.register_filter('cysparse_type_to_numpy_type', cysparse_type_to_numpy_type)
        self.register_filter('cysparse_type_to_numpy_enum_type', cysparse_type_to_numpy_enum_type)
        self.register_filter('cysparse_type_to_real_sum_cysparse_type', cysparse_type_to_real_sum_cysparse_type)
        self.register_filter('cysparse_real_type_from_real_cysparse_complex_type', cysparse_real_type_from_real_cysparse_complex_type)

    ###########################################################################
    # FILE EXTENSIONS
    ###########################################################################
    def register_extension(self, ext_in, ext_out, force=False):
        """
        Add/register a file extension.


        Args:
            ext_in (str): Extension of input files.
            ext_out (str): Extension of corresponding output files.
            force (bool): If ``force`` is set to ``True``, simply overwrite existing extensions, otherwise do nothing.
                If the ``logger`` is set, log a warning about the duplicate extension if ``force == False``.


        """
        if not force and (ext_in in self.__extensions.keys()):
            self.log_warning("Extension %s already exist, ignore redefinition." % ext_in)
            return

        self.__extensions[ext_in] = ext_out

    def register_extensions(self, exts, force=False):
        """
        Add/register extensions.

        Args:
            exts (dict):
            force (bool): If ``force`` is set to ``True``, simply overwrite existing extensions, otherwise do nothing.
                If the ``logger`` is set, log a warning about the duplicate extension if ``force == False``.
        """
        for ext_in, ext_out in exts.items():
            self.register_extension(ext_in, ext_out, force)

    def registered_extensions_list(self):
        """
        Return a list of registered extensions.


        """
        return self.__extensions.keys()

    ###########################################################################
    # ACTIONS
    ###########################################################################
    def __add_action(self, relative_directory, action):
        """
        Add action into the dictionary of actions.

        Args:
            relative_directory:
            action:

        """




    def __retrieve_action(self, relative_directory):
        """
        Return an action corresponding to a relative directory or ``None`` is none is attached to this directory.

        Args:
            relative_directory:

        """

    def register_action(self, relative_directory, file_pattern, action_function):
        """
        Add/register an "action".

        Args:
            relative_directory:
            file_pattern:
            action_function:

        """
        # test if directory exists
        if not os.path.isdir(os.path.join(self.__directory, relative_directory)):
            self.log_error('Relative directory \'%s\' does not exist.' % relative_directory)
            return

        # test if function returns a couple of values
        try:
            for end_string, context in action_function():
                if not isinstance(end_string, basestring):
                    raise RuntimeError
                if not isinstance(context, dict):
                    raise RuntimeError
                break
        except Exception:
            self.log_error('Attached function is not an action function.')

        self.__add_action(relative_directory, GeneratorAction(file_pattern, action_function))

    ###########################################################################
    # FILE GENERATION
    ###########################################################################
    def __generate_file(self, template_filename, context, end_ext, force=False):
        """
        Generate **one** (source code) file from a template.

        The file is **only** generated if needed, i.e. if ``force`` is set to ``True`` or if generated file is older
        than the template file. The generated file is written in the same directory as the template file.

        Args:
            template_filename (str): **Absolute** filename of a template file to translate.
            context (dict): Dictionary with ``(key, val)`` replacements.
            end_ext (str): End extension to add to the generated file filename. For instance '_X_Y.z'.
            force (bool): If set to ``True``, file is generated no matter what.


        """
        base_path, base_filename = os.path.split(template_filename)
        base_filename_without_extension, ext = os.path.splitext(base_filename)

        generated_filename = base_filename_without_extension + '%s' % end_ext
        generated_filename_path = os.path.join(base_path, generated_filename)
        # test if file is non existing or needs to be regenerated
        if force or (not os.path.isfile(generated_filename_path) or os.stat(template_filename).st_mtime - os.stat(generated_filename_path).st_mtime > 1):
            self.log_info('   Parsing file %s' % template_filename)
            code_generated = self.__jinja2_environment.get_template(template_filename).render(context)

            with open(generated_filename_path, 'w') as f:
                self.log_info('   Generating file %s' % generated_filename_path)
                f.write(code_generated)

    # TODO: do we keep this method?
    def __generate_files_list(self, directory,  glob_pattern):
        """
        Return/generate a list of **absolute** filenames
        :param glob_pattern:
        """
    # TODO: erase this temp method
    def generate_file(self, template_filename, context, end_ext, force=False):
        self.__generate_file(template_filename, context, end_ext, force)

    def generate(self, dir_pattern, file_pattern, action='g', recursively=False):
        """
        Main method to generate (source code) files from templates.

        See documentation about the directory and file patterns and their possible combinations.

        Args:
            dir_pattern: ``glob`` pattern taken from the root directory. **Only** used for directories.
            file_pattern: ``fnmatch`` pattern taken from all matching directories. **Only** used for files.
            action (char): Denote action to be taken. Can be:
                - g: Generate all files that match both directory and file patterns. This is the default behavior.
                - d: Same as `g` but with doing anything, i.e. dry run.
                - e: Same as `g` but erasing the generated files instead.
            recursively: Do we do the actions in the sub-directories? Note that in this case **only** the file pattern applies.

        """
        directories = [os.path.abspath(directory) for directory in glob.glob(os.path.join(self.__directory, dir_pattern)) if os.path.isdir(directory)]
        for directory in directories:
            for b, f in find_files(directory, file_pattern, recursively=recursively):
                print b + ': ' + f
                if action == 'd':
                    pass
                elif action == 'g':
                    pass
                elif action == 'd':
                    pass