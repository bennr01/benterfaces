"""miscelaneous test helpers. This should only be used for benterface tests!"""
from zope.interface import Interface, implementer


class ITestPlugin(Interface):
    """A test interface."""
    def get_id(self):
        """return an id string."""
        pass


class IPriorityTestPlugin(Interface):
    """A test interface."""
    def get_id(self):
        """return an id string."""
        pass


class IRequirementTestPlugin(Interface):
    """A test interface."""
    def get_id(self):
        """return an id string."""
        pass


class IDoNotImplement(Interface):
    """An interface to test not implemented interfaces."""
    def do_nothing(self):
        """do nothing."""
        pass


@implementer(ITestPlugin)
class TestPluginForExlusion(object):
    """A test plugin for testing exclusion."""

    def get_id(self):
        return "test_plugin_for_exclusion"


@implementer(ITestPlugin)
class TestPluginForInclusion(object):
    """A test plugin for testing inclusion."""

    def get_id(self):
        return "test_plugin_for_inclusion"
