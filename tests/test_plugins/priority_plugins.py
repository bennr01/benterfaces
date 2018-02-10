"""plugin priority tests."""
from zope.interface import implements

from benterfaces import priority
from benterfaces._test import IPriorityTestPlugin



@priority(10)
class LowPriorityImplementation(object):
    """A low priority plugin."""
    implements(IPriorityTestPlugin)

    def get_id(self):
        """returns the plugin id."""
        return "low_priority_plugin"


@priority(20)
class MediumPriorityImplementation(object):
    """A medium priority plugin."""
    implements(IPriorityTestPlugin)

    def get_id(self):
        """returns the plugin id."""
        return "medium_priority_plugin"


@priority(30)
class HighPriorityImplementation(object):
    """A high priority plugin."""
    implements(IPriorityTestPlugin)

    def get_id(self):
        """returns the plugin id."""
        return "high_priority_plugin"
