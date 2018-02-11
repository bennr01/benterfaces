"""plugin requirements tests."""
from zope.interface import implementer

from benterfaces import requires
from benterfaces._test import IRequirementTestPlugin


@implementer(IRequirementTestPlugin)
class NoRequirementsPlugin(object):
    """plugin without requirement specification."""

    def get_id(self):
        """returns an id string."""
        return "no_requirements_plugin"


@requires(condition=True)
@implementer(IRequirementTestPlugin)
class AlwaysTruePlugin(object):
    """plugin with condition always True requirement specification."""

    def get_id(self):
        """returns an id string."""
        return "always_true_plugin"


@requires(condition=False)
@implementer(IRequirementTestPlugin)
class AlwaysFalsePlugin(object):
    """plugin with condition always False requirement specification."""

    def get_id(self):
        """returns an id string."""
        return "always_false_plugin"


@requires(modules=["unittest"])
@implementer(IRequirementTestPlugin)
class UnittestRequiredPlugin(object):
    """plugin requiring unittest."""

    def get_id(self):
        """returns an id string."""
        return "unittest_required_plugin"


@requires(modules=["does_notExist"])
@implementer(IRequirementTestPlugin)
class NotExistingModuleRequiredPlugin(object):
    """plugin requiring a non-existing module."""

    def get_id(self):
        """returns an id string."""
        return "non_existing_module_required_plugin"


@requires(modules=["unittest", "does_notExist"])
@implementer(IRequirementTestPlugin)
class NotAllModulesRequiredExistingPlugin(object):
    """plugin requiring an existing and a non-existing module."""

    def get_id(self):
        """returns an id string."""
        return "non_existing_and_existing_module_required_plugin"


@requires(condition=False, modules=["unittest"])
@implementer(IRequirementTestPlugin)
class ModulesExistsButConditionIsFalsePlugin(object):
    """plugin requiring an existing module but having a False condition."""

    def get_id(self):
        """returns an id string."""
        return "required_modules_exists_but_condition_is_false_plugin"
