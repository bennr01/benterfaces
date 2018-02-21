"""A test plugin for case specific plugins."""
from zope.interface import Interface, implementer

from benterfaces._test import IUseSpecificTestPlugin
from benterfaces import only_if


def is_value_1(for_):
    """check if for_["value"] == 1"""
    v = for_.get("value", None)
    return v == 1


def is_value_2(for_):
    """check if for_["value"] == 2"""
    v = for_.get("value", None)
    return v == 2


@only_if(is_value_1)
@implementer(IUseSpecificTestPlugin)
class TestImplementationForValue1(object):
    """A test implementation in a .py file."""

    def get_id(self):
        """return an id string."""
        return "test_plugin_for_value_1"


@only_if(is_value_2)
@implementer(IUseSpecificTestPlugin)
class TestImplementationForValue2(object):
    """A test implementation in a .py file."""

    def get_id(self):
        """return an id string."""
        return "test_plugin_for_value_2"
