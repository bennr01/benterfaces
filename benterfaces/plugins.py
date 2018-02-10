"""a plugin system"""
import os
import imp

from zope.interface import implementedBy


class PluginDiscoverer(object):
    """Class for discovering plugins."""
    def __init__(self, paths, extensions=[".py"]):
        self.paths = paths
        self.extensions = extensions
        self.plugins = []

    @property
    def loaded(self):
        """number of loaded plugins, including disabled ones."""
        return len(self.plugins)

    @property
    def enabled(self):
        """number of enabled plugins."""
        enabled = filter(None, [p if check_requirements(p) else None for p in self.plugins])
        return len(enabled)

    def get_all_plugins(self, iface, exclude=[], sorted_by_priority=True):
        """returns a list of all plugins implementing iface."""
        ret = []
        for plugin in self.plugins:
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
        """
        plugins = self.get_all_plugins(iface, exclude=exclude, sorted_by_priority=True)
        if len(plugins) == 0:
            raise NotImplementedError("No (working) implementation found for {iface!r}.".format(iface=iface))
        return plugins[0]

    get_plugin = get_implementation

    def clear_plugin_list(self):
        """clears the internal plugin list."""
        self.plugins = []

    def load_plugins(self, max_depth=9999):
        """loads plugins from the paths"""
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
                    results += self._load_from_path(fp)
        return results

    def _load_from_path(self, path):
        """loads plugins from the file at path"""
        mod = self._load_module_from_path(path)
        results = self._load_from_module(mod)
        return results

    def _load_module_from_path(self, path):
        """loads a module from a given path."""
        print "loading: ", path
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
    Arguments:
        condition: A boolean. This can be used for custom requirements.
        modules: A list of module names required for this plugin.
    Returns:
        A decorator function.
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
    """
    def wrapper(cls):
        cls._plugin_priority = n
        return cls
    return wrapper


def get_priority(cls):
    """returns the priority of a plugin."""
    if not hasattr(cls, "_plugin_priority"):
        return 0
    return cls._plugin_priority
