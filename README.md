# benterfaces - Interface utilities and plugin system
[![Travis](https://img.shields.io/travis/bennr01/benterfaces.svg)]()
[![Coveralls github](https://img.shields.io/coveralls/github/bennr01/benterfaces.svg)]()
[![GitHub issues](https://img.shields.io/github/issues/bennr01/benterfaces.svg)](https://github.com/bennr01/benterfaces/issues)
[![GitHub license](https://img.shields.io/github/license/bennr01/benterfaces.svg)](https://github.com/bennr01/benterfaces/blob/master/LICENSE)


`benterfaces` contains miscellaneous interface utilities and a plugin system.

# Interface utilities
**@verify_implementation**
A simple decorator for verifying interface implementations when a class is created.
For example, the following code would raise a BrokenImplementationError if FooBar would not implement IFoo or IBar correctly.

```python
from zope.interfaces import implementer
from benterfaces import verify_implementation

from imyproject import IFoo, IBar


@verify_implementation
@implementer(IFoo, IBar)
class FooBar(object):
    ...


```

This is useful if your interfaces may change during the developement process.
Also, its a single line (+import), so its not much work to add.


# Plugin system
The plugin system provides an easy way to make your scripts extendandable.
Here is a list of some features of the plugin system:
- plugin priority support (you can use this feature to allow plugins to overwrite each other)
- plugin requirement support (enable/disable plugins depending on conditions and installed modules)
- load plugins from multiple paths
- load plugins from python source files of any file extension
- load plugins from `.pyc`-files


**PluginDiscoverer(paths, extensions=[".py"])**

This class handles the plugin discovery and loading.
Arguments:
- `paths`: list of strings specifying directories to search for plugins.
- `extensions`: list of file extensions in which plugins will be searched for.

Important methods and attributes:
- `load_plugins(max_depth=9999)`: load plugins from self.paths. Descend at most `max_depth` directories.
- `loaded`: number of loaded plugins
- `enabled`: number of enabled plugins
- `clear_plugin_list()`: clears the internal plugin cache.
- `get_implementation(self, iface, exclude=[])`: returns the plugin implementing `iface` with the highest priority which is not in `exclude`. This raises a `NotImplementedError` if no plugin if found.
- `get_plugin(...)`: same as `get_implementation()`.
- `get_all_plugins(self, iface, exclude=[], sorted_by_priority=True)`: returns a list of all plugins implementing iface excluding `exclude`.


**@requires(condition=True, modules=[])**

This decorator function marks the requirements of a plugin.
Arguments:
- `condition`: a boolean which must be `True` in order for the plugin to be enabled.
- `modules`: a list of module names which are required for the plugin to be enabled.
Plugins without a `@requires(...)` decorator are always enabled.


**@priority(n=0)**

This decorator function sets the priority of a plugin.
Higher values for `n` mean a higher priority.
Plugins without a `@priority(...)` decorator are considered to have a priority of `0`.


# Using plugins
**Creating a plugin**
Creating a plugin is simple:
1. create a file containing a `zope.interface.Interface`-definition which can be imported from your project and the plugin directory.
2. create one or more plugin directories
3. create a `.py` file inside the plugin directory containing an implementation of the plugin (remember to implement the Interface)
4. Done.

**loading plugins**
To load your plugins, just do the following:
1. import `benterfaces.PluginDiscoverer()`
2. create an instance of `benterfaces.PluginDiscoverer(paths)`, passing the plugin directories as `paths`.
3. call the `.load_plugins()` method of the instance.
4.  Depending on your use case, use `get_plugin(iface)` or `get_all_plugins(iface)` to access the plugins.
