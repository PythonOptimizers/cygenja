from __future__ import print_function

import jinja2
import os
import glob
import fnmatch

from cygenja.filters.type_filters import *
from cygenja.helpers.file_helpers import find_files
from cygenja.treemap.treemap import TreeMap


class GeneratorAction(object):
    def __init__(self, file_pattern, action_function):
        """
        Container to store an "action".

        Every file(s) generation is considered as an action.

        Args:
            file_pattern: fnmatch pattern.
            action_function: Callback without argument. See documentation.
        """
        super(GeneratorAction, self).__init__()
        self.__file_pattern = file_pattern
        self.__action_function = action_function

    def run(self):
        return self.__action_function()

    def action_function_name(self):
        return self.__action_function.__name__

    def act_on_file(self, filename):
        return fnmatch.fnmatch(filename, self.__file_pattern)


class GeneratorActionContainer(object):
    def __init__(self):
        """
        Container to store :class:`GeneratorAction` objects.

        A :class:`GeneratorActionContainer` is attached with one directory.

        """
        super(GeneratorActionContainer, self).__init__()
        self.__generator_actions = list()

    def add_generator_action(self, action):
        """
        Attach/add one :class:`GeneratorAction`.

        Warning:
            The order in which you add :class:`GeneratorAction` objects **is** important in case of conflicting :class:`GeneratorAction` objects:
            **only** the **first compatible** :class:`GeneratorAction` object will be used to generate the (source code) files.
        """
        if not isinstance(action, GeneratorAction):
            raise RuntimeError('Can not add a none GeneratorAction object.')

        self.__generator_actions.append(action)

    def get_compatible_generator_action(self, filename):
        """
        Return the **first** compatible :class:`GeneratorAction` for a given filename or ``None`` if none is found.

        Args:
            filename (str): The filename of the template to process.
        """
        # find first compatible generator action
        for action in self.__generator_actions:
            if action.act_on_file(filename):
                return action

        return None


class Generator(object):
    """
    (Code source) file generator.

    This is the main class for :program:`cygenja`. See documentation.


    """
    def __init__(self, directory, jinja2_environment, logger=None, raise_exception_on_warning=False):
        """
        Constructor of a :program:`cygenja` template machine.

        Args:
            directory (str): Absolute or relative base directory. Everything happens in that directory and sub-directories.
            jinja2_environment: :program:`Jinja2` environment.
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

        self.__root_directory = os.path.abspath(directory)   # main base directory
        self.__jinja2_environment = jinja2_environment



        self.__jinja2_predefined_filters = self.__jinja2_environment.filters.keys()



        self.__extensions = {}
        self.__actions = TreeMap()

        self.__default_action = None

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
    # INFO
    ###########################################################################
    def root_directory(self):
        """
        Return root directory as absolute path.

        """
        return self.__root_directory

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

    # TODO: transform names and put in POCS
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
        generator_action_container = self.__actions.retrieve_element_or_default(relative_directory, None)

        if generator_action_container is None:
            generator_action_container = GeneratorActionContainer()
            generator_action_container.add_generator_action(action)
            self.__actions.add_element(location=relative_directory, element=generator_action_container)
        else:
            generator_action_container.add_generator_action(action)

    def __retrieve_generator_action_container(self, relative_directory):
        """
        Return an :class:`GeneratorActionContainer` corresponding to a relative directory or ``None`` is none is attached to this directory.

        Args:
            relative_directory:

        """
        return self.__actions.retrieve_element_or_default(relative_directory)

    def __is_function_action(self, action_function):
        """
        Detect if given function is really an action function.

        Args:
            action_function: Function to test.

        Note:
            We don't care if the variable refer to a function but rather if it is callable or not.

        """
        # test if function returns a couple of values
        is_function_action = True

        if not hasattr(action_function, '__call__'):
            return False

        # OK, callable. Do we receive the right arguments?
        try:
            for end_string, context in action_function():
                if not isinstance(end_string, basestring):
                    self.log_error("Action function must return end of filename as a string as first argument")
                if not isinstance(context, dict):
                    self.log_error("Action function must return context as a dict as second argument")
                break
        except Exception:
            is_function_action = False

        return is_function_action

    def register_action(self, relative_directory, file_pattern, action_function):
        """
        Add/register an "action".

        Args:
            relative_directory (str): Relative directory from root directory. Separator is OS dependent. For instance,
                under linux, you can register the following:

                >>> register_action('cysparse/sparse/utils', 'find*.cpy', action_function)

                This means that all files corresponding to the `'find*.cpy'` pattern inside the `cysparse/sparse/utils`
                directory can (see Warning) be dealt with the `action_function`.

            file_pattern: A :program:`fnmatch` pattern for the files concerned by this action.
            action_function: A callback without argument. See documentation.

        Warning:
            The order in which you add actions is important. A file will be dealt with the **first** compatible
            action found.
        """
        # test if directory exists
        if not os.path.isdir(os.path.join(self.__root_directory, relative_directory)):
            self.log_error('Relative directory \'%s\' does not exist.' % relative_directory)
            return

        if not self.__is_function_action(action_function):
                self.log_error('Attached function is not an action function.')

        self.__add_action(relative_directory, GeneratorAction(file_pattern, action_function))

    def register_default_action(self, file_pattern,  action_function):
        """
        Default action used if no compatible action is found.

        Args:
            file_pattern: A :program:`fnmatch` pattern for the files concerned by this action.
            action_function:

        Warning:
            Be careful when defining a default action. This action is be applied to **all** template files for
            which no compatible action is found. You might want to prefer declare explicit actions than to rely on this
            implicit default action. Use at your own risks. That said, if you have lots of default cases, this
            default action can be very convenient and avoid lots of unnecessary action declarations.
        """
        if self.__default_action is not None:
            self.log_error('Default action function already exist.')

        if not self.__is_function_action(action_function):
            self.log_error('Attached default function is not an action function.')

        self.__default_action = GeneratorAction(file_pattern=file_pattern, action_function=action_function)

    def registered_actions_treemap(self):
        """
        Return a list of registered actions.


        """
        return self.__actions

    ###########################################################################
    # FILE GENERATION
    ###########################################################################
    def __generate_file(self, template_filename, context, generated_filename, force=False):
        """
        Generate **one** (source code) file from a template.

        The file is **only** generated if needed, i.e. if ``force`` is set to ``True`` or if generated file is older
        than the template file. The generated file is written in the same directory as the template file.

        Args:
            template_filename (str): **Absolute** filename of a template file to translate.
            context (dict): Dictionary with ``(key, val)`` replacements.
            generated_filename (str): **Absolute** filename of the generated file filename.
            force (bool): If set to ``True``, file is generated no matter what.


        """
        # TODO: maybe avoid reading same template file again and again... i.e. parse it once and generate all needed files without reparsing the template.
        # test if file is non existing or needs to be regenerated
        if force or (not os.path.isfile(generated_filename) or os.stat(template_filename).st_mtime - os.stat(generated_filename).st_mtime > 1):
            self.log_info('   Parsing file %s' % template_filename)
            code_generated = self.__jinja2_environment.get_template(template_filename).render(context)

            with open(generated_filename, 'w') as f:
                self.log_info('   Generating file %s' % generated_filename)
                f.write(code_generated.encode('utf8'))

    def generate(self, dir_pattern, file_pattern, action_ch='g', recursively=False, force=False):
        """
        Main method to generate (source code) files from templates.

        See documentation about the directory and file patterns and their possible combinations.

        Args:
            dir_pattern: ``glob`` pattern taken from the root directory. **Only** used for directories.
            file_pattern: ``fnmatch`` pattern taken from all matching directories. **Only** used for files.
            action (char): Denote action to be taken. Can be:
                - g: Generate all files that match both directory and file patterns. This is the default behavior.
                - d: Same as `g` but with doing anything, i.e. dry run.
                - c: Same as `g` but erasing the generated files instead, i.e. clean.
            recursively: Do we do the actions in the sub-directories? Note that in this case **only** the file pattern applies as **all**
                the subdirectories are visited.
            force (boolean): Do we force the generation or not?

        """
        # directories to visit
        # using heavy machinery to extract absolute cleaned paths... to avoid any problem...
        directories = [os.path.abspath(directory) for directory in glob.glob(os.path.join(self.__root_directory, dir_pattern)) if os.path.isdir(directory)]

        # list of extensions
        extensions = self.__extensions.keys()

        for directory in directories:
            for b, f in find_files(directory, file_pattern, recursively=recursively):
                # test if some template files can be processed
                file_basename, file_ext = os.path.splitext(f)

                if file_ext in extensions:
                    # try to find corresponding action
                    rel_path = os.path.relpath(os.path.join(b,f), self.__root_directory)
                    rel_basename, rel_filename = os.path.split(rel_path)
                    rel_filename_without_ext, rel_ext = os.path.splitext(rel_filename)

                    # template absolute filename
                    in_file_name = os.path.join(b, f)

                    generator_action_container = self.__actions.retrieve_element_or_default(rel_basename, None)
                    action = None

                    if generator_action_container is not None:
                        action = generator_action_container.get_compatible_generator_action(f)

                    # is there a default action if needed?
                    if action is None:
                        action = self.__default_action

                    if action:

                        if action_ch == 'd':
                            print("Process file '%s' with function '%s':" % (rel_path, action.action_function_name()))
                        for filename_end, context in action.run():
                            # generated absolute file name
                            out_file_name = os.path.join(b, rel_filename_without_ext + filename_end + self.__extensions[file_ext])
                            if action_ch == 'g':
                                self.__generate_file(template_filename=in_file_name, context=context, generated_filename=out_file_name, force=force)
                            elif action_ch == 'c':
                                try:
                                    os.remove(out_file_name)
                                    self.log_info("Removed file '%s'" % out_file_name)
                                except OSError:
                                    pass
                            elif action_ch == 'd':
                                # we only print relative path
                                print("   -> %s" % os.path.join(rel_basename, rel_filename_without_ext + filename_end + self.__extensions[file_ext]))


