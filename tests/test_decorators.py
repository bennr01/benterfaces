"""Tests for benterfaces.decorators"""
from zope.interface import Interface, implementer, Attribute
from zope.interface.verify import BrokenImplementation

from benterfaces import verify_implementation


class InterfaceA(Interface):
    """Test Interface A"""

    attribute_a = Attribute("a test attribute")

    def method_a():
        """test method b"""
        pass


class InterfaceB(Interface):
    """Test Interface B"""

    attribute_a = Attribute("b test attribute")

    def method_b():
        """test method b"""
        pass



def test_valid_implementation_single():
    """test verify_implementation() handling of a valid single interface class."""

    # create valid implementation
    @verify_implementation
    @implementer(InterfaceA)
    class ImplementerA(object):
        """test implementation."""

        attribute_a = 2

        def method_a(self):
            """test implementation."""
            return self.attribute_a ** self.attribute_a


def test_invalid_method_implementation_single():
    """test verify_implementation() handling of a missing method in a single interface class."""
    try:
        # this should fail

        # create an invalid implementation without method_a()
        @verify_implementation
        @implementer(InterfaceA)
        class ImplementerA(object):
            """test implementation."""

            attribute_a = 2

            def not_method_a(self):
                """test implementation."""
                return self.attribute_a ** self.attribute_a

    except BrokenImplementation:
        # expected
        pass

    else:
        # this should have failed
        raise AssertionError("verify_implementation() did not fail on missing method!")


'''
def test_invalid_attribute_implementation_single():
    """test verify_implementation() handling of a missing attribute in a single interface class."""
    try:
        # this should fail

        # create an invalid implementation without attribute_a
        @verify_implementation
        @implementer(InterfaceA)
        class ImplementerA(object):
            """test implementation."""

            not_attribute_a = 2

            def method_a(self):
                """test implementation."""
                return self.not_attribute_a ** self.not_attribute_a

    except BrokenImplementation:
        # expected
        pass

    else:
        # this should have failed
        raise AssertionError("verify_implementation() did not fail on missing attribute!")
'''


def test_valid_implementation_multi():
    """test verify_implementation() handling of a valid multi interface class."""

    @verify_implementation
    @implementer(InterfaceA, InterfaceB)
    class ImplementerAB(object):
        """test implementation."""

        attribute_a = 2
        attribute_b = 3

        def method_a(self):
            """test implementation."""
            return self.attribute_a ** self.attribute_a

        def method_b(self):
            """test implementation."""
            return self.attribute_b ** self.attribute_b


'''
def test_invalid_attribute_1_implementation_multi():
    """test verify_implementation() handling of an invalid multi interface class."""
    try:
        # this should fail
        @verify_implementation
        @implementer(InterfaceA, InterfaceB)
        class ImplementerAB(object):
            """test implementation."""

            attribute_a = 2
            not_attribute_b = 3

            def method_a(self):
                """test implementation."""
                return self.attribute_a ** self.attribute_a

            def method_b(self):
                """test implementation."""
                return self.not_attribute_b ** self.not_attribute_b

    except BrokenImplementation:
        # expected
        pass

    else:
        # this should have failed
        raise AssertionError("verify_implementation() did not fail on missing attribute in multi interface implementation!")


def test_invalid_attribute_2_implementation_multi():
    """test verify_implementation() handling of an invalid multi interface class."""
    try:
        # this should fail
        @verify_implementation
        @implementer(InterfaceA, InterfaceB)
        class ImplementerAB(object):
            """test implementation."""

            not_attribute_a = 2
            attribute_b = 3

            def method_a(self):
                """test implementation."""
                return self.not_attribute_a ** self.not_attribute_a

            def method_b(self):
                """test implementation."""
                return self.attribute_b ** self.attribute_b

    except BrokenImplementation:
        # expected
        pass

    else:
        # this should have failed
        raise AssertionError("verify_implementation() did not fail on missing attribute in multi interface implementation!")
'''


def test_invalid_method_1_implementation_multi():
    """test verify_implementation() handling of an invalid multi interface class."""
    try:
        # this should fail
        @verify_implementation
        @implementer(InterfaceA, InterfaceB)
        class ImplementerAB(object):
            """test implementation."""

            attribute_a = 2
            attribute_b = 3

            def not_method_a(self):
                """test implementation."""
                return self.attribute_a ** self.attribute_a

            def method_b(self):
                """test implementation."""
                return self.attribute_b ** self.attribute_b

    except BrokenImplementation:
        # expected
        pass

    else:
        # this should have failed
        raise AssertionError("verify_implementation() did not fail on missing attribute in multi interface implementation!")


def test_invalid_method_2_implementation_multi():
    """test verify_implementation() handling of an invalid multi interface class."""
    try:
        # this should fail
        @verify_implementation
        @implementer(InterfaceA, InterfaceB)
        class ImplementerAB(object):
            """test implementation."""

            attribute_a = 2
            attribute_b = 3

            def method_a(self):
                """test implementation."""
                return self.attribute_a ** self.attribute_a

            def not_method_b(self):
                """test implementation."""
                return self.attribute_b ** self.attribute_b

    except BrokenImplementation:
        # expected
        pass

    else:
        # this should have failed
        raise AssertionError("verify_implementation() did not fail on missing attribute in multi interface implementation!")

