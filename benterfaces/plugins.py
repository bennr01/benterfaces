"""a plugin system"""
import os
import imp

from zope.interface import implementedBy


class PluginDiscoverer(object):
    """
    Class for discovering plugins.
    :param paths: paths which should be searched for plugins
    :type paths: list
    :param extensions: only files whose extensions are in this list will be searched for plugins
    :type paths: list
    :param ignore_errors: wether to silently handle errors when loading plugins
    :type ignore_errors: boolean
    :param defaults: list of plugins which will be included in the results
    :type defaults: list
    """
    def __init__(self, paths, extensions=[".py"], ignore_errors=False, include=[]):
        assert isinstance(paths, list), "expected a list of paths!"
        assert isinstance(extensions, list), "expected a list of extensions!"
        assert isinstance(include, list)
        self.paths = paths
        self.extensions = extensions
        self.include = include
        self._ignore_errors = ignore_errors
        self.plugins = []
        self._error_paths = []

    @property
    def loaded(self):
        """
        Number of loaded plugins, including disabled ones.
        This does not include plugins from 'self.include'.
        """
        return len(self.plugins)

    @property
    def enabled(self):
        """
        Number of enabled plugins.
        This does not include plugins  from 'self.include'.
        """
        enabled = list(filter(None, [p if check_requirements(p) else None for p in self.plugins]))
        return len(enabled)

    @property
    def errors(self):
        """
        Number of errors when tried to load plugins.
        """
        return len(self._error_paths)

    @property
    def error_paths(self):
        """
        List of paths which could not be loaded.
        """
        return self._error_paths

    def get_all_plugins(self, iface, exclude=[], sorted_by_priority=True):
        """
        Returns a list of all plugins implementing iface.
        :param iface: iface for which plugins will be searched.
        :type iface: zope.interface.Interface
        :param exclude: plugins which will not be returned from this list.
        :type exclude: list
        :param sorted_by_priority: wether the plugins should be returned in priority order (highest priority first)
        :type sorted_by_priority: boolean
        :return: list of plugins
        :rtype: list
        """
        ret = []
        plugins = self.plugins + self.include
        for plugin in plugins:
            if plugin in exclude:
                continue
            if not iface.implementedBy(plugin):
                continue
            if check_requirements(plugin):
                ret.append(plugin)

        if sorted_by_priority:
            ret.sort(key=get_priority, reverse=True)
        return ret

    def get_implementation(self, iface, exclude=[]):
        """
        Returns an implementation of iface, excluding any implementation in excluding.
        Raises NotImplementedError if None is found.
        :param iface: iface for which plugins will be searched.
        :type iface: zope.interface.Interface
        :param exclude: plugins which will not be returned from this list.
        :type exclude: list
        :return: the plugin with the heighest priority
        :rtype: object
        :raises: NotImplementedError if no plugin implements iface
        """
        plugins = self.get_all_plugins(iface, exclude=exclude, sorted_by_priority=True)
        if len(plugins) == 0:
            raise NotImplementedError("No (working) implementation found for {iface!r}.".format(iface=iface))
        return plugins[0]

    get_plugin = get_implementation

    def is_implemented(self, iface, exclude=[]):
        """
        Returns True if there is an implementation of iface which is not in excluding.
        Returns False otherwise.
        """
        plugins = self.get_all_plugins(iface, exclude=exclude, sorted_by_priority=False)
        if len(plugins) == 0:
            return False
        else:
            return True

    def clear_plugin_list(self):
        """clear the internal plugin list."""
        self.plugins = []
        self._error_paths = []

    def reload_plugins(self):
        """clear the internal plugin list and reload all plugins."""
        self.clear_plugin_list()
        self.load_plugins()

    def load_plugins(self, max_depth=9999):
        """
        Load plugins from the paths.
        This may raise exceptions or errors if self._ignore_errors is False.
        :param max_depth: how deep to descend into subdirectories
        :type max_depth: int
        """
        for p in self.paths:
            plugins = self._search_dir(p, max_depth=max_depth)
            for pl in plugins:
                if pl not in self.plugins:
                    self.plugins.append(pl)

    def _search_dir(self, path, max_depth=9999):
        """searches a path for plugins."""
        results = []
        for fn in os.listdir(path):
            fp = os.path.join(path, fn)
            if os.path.isdir(fp) and max_depth >= 1:
                results += self._search_dir(fp, max_depth - 1)
            else:
                filename, extension = os.path.splitext(fn)
                if (self.extensions is None) or (extension in self.extensions):
                    try:
                        results += self._load_from_path(fp)
                    except (Exception, SyntaxError) as e:
                        self._error_paths.append(fp)
                        if not self._ignore_errors:
                            raise e
        return results

    def _load_from_path(self, path):
        """loads plugins from the file at path"""
        mod = self._load_module_from_path(path)
        results = self._load_from_module(mod)
        return results

    def _load_module_from_path(self, path):
        """loads a module from a given path."""
        filename, extension = os.path.splitext(path)
        if extension == ".pyc":
            return imp.load_compiled(filename, path)
        else:
            return imp.load_source(filename, path)

    def _load_from_module(self, mod, ignore_private=True):
        """searches for plugins in the given module."""
        results = []
        for on in dir(mod):
            obj = getattr(mod, on)
            if on.startswith("_") and ignore_private:
                continue
            implements = list(implementedBy(obj))
            if len(implements) == 0:
                continue
            results.append(obj)
        return results


def requires(condition=True, modules=[]):
    """
    Marks the requirements of a plugin.
    This should be used as a decorator.
    The arguments describe these requirements.
    A plugin will only be used if ALL the requirements are met.
    :param condition: boolean which needs to be True in order to fulfil this requirement
    :type condition: boolean
    :param modules: A list of module names required for this plugin.
    :type modules: list
    :return: A decorator function.
    :rtype: function
    """
    requirements = {
        "condition": condition,
        "modules": modules,
        }

    def wrapper(cls):
        cls._plugin_requirements = requirements
        return cls

    return wrapper


def check_requirements(cls):
    """checks the requirements of a plugin."""
    if not hasattr(cls, "_plugin_requirements"):
        # no requirements marked.
        return True
    requirements = cls._plugin_requirements

    # check boolean condition
    if not requirements["condition"]:
        return False

    # check module requirements
    for mn in requirements["modules"]:
        try:
            imp.find_module(mn)
        except ImportError:
            return False

    # all checks done, seems like we can use this plugin
    return True


def priority(n=0):
    """
    Sets the priority of the plugin.
    Higher values indicate a higher priority.
    This should be used as a decorator.
    Returns a decorator function.
    :param n: priority (higher values = higher priority)
    :type n: int
    :rtype: function
    """
    def wrapper(cls):
        cls._plugin_priority = n
        return cls
    return wrapper


def get_priority(cls):
    """
    Returns the priority of a plugin.
    :param cls: class to get priority from
    :type cls: class
    :return: the priority of cls
    :rtype: int
    """
    if not hasattr(cls, "_plugin_priority"):
        return 0
    return cls._plugin_priority
