"""plugin requirements tests."""
from zope.interface import implements

from benterfaces import requires
from benterfaces._test import IRequirementTestPlugin


class NoRequirementsPlugin(object):
    """plugin without requirement specification."""

    implements(IRequirementTestPlugin)

    def get_id(self):
        """returns an id string."""
        return "no_requirements_plugin"


@requires(condition=True)
class AlwaysTruePlugin(object):
    """plugin with condition always True requirement specification."""

    implements(IRequirementTestPlugin)

    def get_id(self):
        """returns an id string."""
        return "always_true_plugin"


@requires(condition=False)
class AlwaysFalsePlugin(object):
    """plugin with condition always False requirement specification."""

    implements(IRequirementTestPlugin)

    def get_id(self):
        """returns an id string."""
        return "always_false_plugin"


@requires(modules=["unittest"])
class UnittestRequiredPlugin(object):
    """plugin requiring unittest."""

    implements(IRequirementTestPlugin)

    def get_id(self):
        """returns an id string."""
        return "unittest_required_plugin"


@requires(modules=["does_notExist"])
class NotExistingModuleRequiredPlugin(object):
    """plugin requiring a non-existing module."""

    implements(IRequirementTestPlugin)

    def get_id(self):
        """returns an id string."""
        return "non_existing_module_required_plugin"


@requires(modules=["unittest", "does_notExist"])
class NotAllModulesRequiredExistingPlugin(object):
    """plugin requiring an existing and a non-existing module."""

    implements(IRequirementTestPlugin)

    def get_id(self):
        """returns an id string."""
        return "non_existing_and_existing_module_required_plugin"


@requires(condition=False, modules=["unittest"])
class ModulesExistsButConditionIsFalsePlugin(object):
    """plugin requiring an existing module but having a False condition."""

    implements(IRequirementTestPlugin)

    def get_id(self):
        """returns an id string."""
        return "required_modules_exists_but_condition_is_false_plugin"
