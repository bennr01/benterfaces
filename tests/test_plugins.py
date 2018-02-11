"""Tests for benterfaces.decorators"""
import os

try:
    from unittest import skipIf
except ImportError:
    def skipIf(condition, desc):
        if condition:
            print("skipping: " + desc)
            return lambda f: (lambda: None)
        else:
            return lambda f: f

try:
    import py_compile
except ImportError:
    py_compile = None

from zope.interface import implements
from zope.interface.verify import BrokenImplementation

from benterfaces import PluginDiscoverer, verify_implementation
from benterfaces._test import ITestPlugin, IDoNotImplement
from benterfaces._test import TestPluginForExlusion, IPriorityTestPlugin
from benterfaces._test import IRequirementTestPlugin


TEST_PATH = os.path.dirname(__file__)
TEST_PLUGIN_PATH = os.path.join(TEST_PATH, "test_plugins")
TEST_TXT_PLUGIN_PATH = os.path.join(TEST_PATH, "txt_plugins")
TEST_PYC_PLUGIN_PATH = os.path.join(TEST_PATH, "pyc_test_plugins")
TEST_PYC_RAW_PLUGIN_PATH = os.path.join(TEST_PYC_PLUGIN_PATH, "testplugin.py")



def get_discoverer():
    """returns a PluginDiscoverer."""
    discoverer = PluginDiscoverer([TEST_PLUGIN_PATH])
    return discoverer


def get_plugin(iface, max_depth=9999):
    """returns a plugin implementing iface."""
    discoverer = get_discoverer()
    discoverer.load_plugins(max_depth=max_depth)
    return discoverer.get_plugin(iface)


def test_discover():
    """tests discovery of plugins."""
    discoverer = get_discoverer()
    assert discoverer.loaded == 0
    assert discoverer.enabled == 0
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0


def test_clear_plugin_list():
    """test PluginDiscoverer.clear_plugin_list()."""
    discoverer = get_discoverer()
    assert discoverer.loaded == 0
    assert discoverer.enabled == 0
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0
    discoverer.clear_plugin_list()
    assert discoverer.loaded == 0
    assert discoverer.enabled == 0
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0


def test_reload_plugins():
    """test PluginDiscoverer.reload_plugins()."""
    discoverer = get_discoverer()
    assert discoverer.loaded == 0
    assert discoverer.enabled == 0
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0
    old_loaded = discoverer.loaded
    old_enabled = discoverer.enabled
    discoverer.clear_plugin_list()
    assert discoverer.loaded == 0
    assert discoverer.enabled == 0
    discoverer.reload_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0
    # number of plugins should not have changed
    assert discoverer.loaded == old_loaded
    assert discoverer.enabled == old_enabled


def test_not_implemented_plugins():
    """ensure loading of not implemented plugins fails with NotImplementedError"""
    discoverer = get_discoverer()
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0
    try:
        # this should fail
        plugin = discoverer.get_implementation(IDoNotImplement)
    except NotImplementedError:
        # expected
        pass
    else:
        # test failed
        raise AssertionError("loading of a not implemented plugin did not fail in a NotImplementedError!")


def test_get_all_plugins_exclusion():
    """ensure get_all_plugins(exlude=[...]) works."""
    discoverer = get_discoverer()
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0
    plugins_without_exclusion = discoverer.get_all_plugins(ITestPlugin)
    assert len(plugins_without_exclusion) > 0
    assert TestPluginForExlusion in plugins_without_exclusion
    plugins_with_exclusion = discoverer.get_all_plugins(ITestPlugin, exclude=[TestPluginForExlusion])
    assert TestPluginForExlusion not in plugins_with_exclusion


def test_priority():
    """test plugin priority handling."""
    discoverer = get_discoverer()
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0
    pi = discoverer.get_plugin(IPriorityTestPlugin)()
    assert pi.get_id() == "high_priority_plugin"


def test_requirements_condition():
    """test plugin condition requirements."""
    discoverer = get_discoverer()
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0
    assert discoverer.loaded != discoverer.enabled  # a few plugins should be disabled
    plugins = discoverer.get_all_plugins(IRequirementTestPlugin)
    ids = [p().get_id() for p in plugins]
    assert "no_requirements_plugin" in ids
    assert "always_true_plugin" in ids
    assert "always_false_plugin" not in ids


def test_requirements_modules():
    """test plugin module requirements ."""
    discoverer = get_discoverer()
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0
    assert discoverer.loaded != discoverer.enabled  # a few plugins should be disabled
    plugins = discoverer.get_all_plugins(IRequirementTestPlugin)
    ids = [p().get_id() for p in plugins]
    assert "unittest_required_plugin" in ids
    assert "non_existing_module_required_plugin" not in ids
    assert "non_existing_and_existing_module_required_plugin" not in ids
    assert "required_modules_exists_but_condition_is_false_plugin" not in ids


def test_discover_ignore_txt():
    """tests that files ending with .txt are ignored if not told."""
    discoverer = PluginDiscoverer([TEST_TXT_PLUGIN_PATH], extensions=[".py"])
    assert discoverer.loaded == 0
    assert discoverer.enabled == 0
    discoverer.load_plugins()
    assert discoverer.loaded == 0
    assert discoverer.enabled == 0


def test_discover_include_txt():
    """tests that files ending with .txt are loaded if specified."""
    discoverer = PluginDiscoverer([TEST_TXT_PLUGIN_PATH], extensions=[".txt"])
    discoverer.load_plugins()
    loaded = discoverer.loaded
    enabled = discoverer.enabled
    assert loaded > 0
    assert enabled > 0
    plugin = discoverer.get_implementation(ITestPlugin)
    assert ITestPlugin.implementedBy(plugin)
    pi = plugin()
    assert pi.get_id() == "test_txt_plugin"


@skipIf((py_compile is None), "py_compile not found")
def test_load_compiled():
    """test for loading .pyc plugins."""
    discoverer = PluginDiscoverer(paths=[TEST_PYC_PLUGIN_PATH], extensions=[".pyc", ".pyo"])

    # if old compiled module exists, delete it
    outpath = TEST_PYC_RAW_PLUGIN_PATH + "c"  # see py_compile.compile() defaults
    if os.path.exists(outpath):
        os.remove(outpath)

    # test that .py wont be loaded
    discoverer.load_plugins(max_depth=0)
    assert discoverer.loaded == 0
    assert discoverer.enabled == 0

    # compile module
    py_compile.compile(TEST_PYC_RAW_PLUGIN_PATH, cfile=outpath)

    # test that .pyc will be loaded
    discoverer.load_plugins(max_depth=0)
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0

    # test plugin
    plugin = discoverer.get_implementation(ITestPlugin, exclude=[TestPluginForExlusion])
    pi = plugin()
    assert pi.get_id() == "test_pyc_plugin"


def test_is_implemented():
    """test is_implemented()"""
    discoverer = get_discoverer()
    assert discoverer.loaded == 0
    assert discoverer.enabled == 0
    assert not discoverer.is_implemented(ITestPlugin)
    assert not discoverer.is_implemented(IDoNotImplement)
    discoverer.load_plugins()
    assert discoverer.loaded > 0
    assert discoverer.enabled > 0
    assert discoverer.is_implemented(ITestPlugin)
    assert not discoverer.is_implemented(IDoNotImplement)
