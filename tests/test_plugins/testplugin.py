"""A test plugin."""
from zope.interface import Interface, implementer

from benterfaces._test import ITestPlugin, TestPluginForExlusion


@implementer(ITestPlugin)
class TestImplementation(object):
    """A test implementation in a .py file."""

    def get_id(self):
        """return an id string."""
        return "test_py_plugin"

# create reference in this namespace for TestPluginForExlusion
TestPluginForExlusionReference = TestPluginForExlusion
