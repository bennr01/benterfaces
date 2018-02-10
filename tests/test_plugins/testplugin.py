"""A test plugin."""
from zope.interface import Interface, implements

from benterfaces._test import ITestPlugin, TestPluginForExlusion


class TestImplementation(object):
    """A test implementation in a .py file."""
    implements(ITestPlugin)

    def get_id(self):
        """return an id string."""
        return "test_py_plugin"

# create reference in this namespace for TestPluginForExlusion
TestPluginForExlusionReference = TestPluginForExlusion
