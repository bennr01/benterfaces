"""plugin priority tests."""
from zope.interface import implementer

from benterfaces import priority
from benterfaces._test import IPriorityTestPlugin



@priority(10)
@implementer(IPriorityTestPlugin)
class LowPriorityImplementation(object):
    """A low priority plugin."""

    def get_id(self):
        """returns the plugin id."""
        return "low_priority_plugin"


@priority(20)
@implementer(IPriorityTestPlugin)
class MediumPriorityImplementation(object):
    """A medium priority plugin."""

    def get_id(self):
        """returns the plugin id."""
        return "medium_priority_plugin"


@priority(30)
@implementer(IPriorityTestPlugin)
class HighPriorityImplementation(object):
    """A high priority plugin."""

    def get_id(self):
        """returns the plugin id."""
        return "high_priority_plugin"
