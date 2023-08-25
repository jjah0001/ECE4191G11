# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robot_interfaces:msg/EncoderInfo.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_EncoderInfo(type):
    """Metaclass of message 'EncoderInfo'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('robot_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'robot_interfaces.msg.EncoderInfo')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__encoder_info
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__encoder_info
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__encoder_info
            cls._TYPE_SUPPORT = module.type_support_msg__msg__encoder_info
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__encoder_info

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class EncoderInfo(metaclass=Metaclass_EncoderInfo):
    """Message class 'EncoderInfo'."""

    __slots__ = [
        '_left_count',
        '_right_count',
        '_left_vel',
        '_right_vel',
    ]

    _fields_and_field_types = {
        'left_count': 'int64',
        'right_count': 'int64',
        'left_vel': 'double',
        'right_vel': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int64'),  # noqa: E501
        rosidl_parser.definition.BasicType('int64'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.left_count = kwargs.get('left_count', int())
        self.right_count = kwargs.get('right_count', int())
        self.left_vel = kwargs.get('left_vel', float())
        self.right_vel = kwargs.get('right_vel', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.left_count != other.left_count:
            return False
        if self.right_count != other.right_count:
            return False
        if self.left_vel != other.left_vel:
            return False
        if self.right_vel != other.right_vel:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def left_count(self):
        """Message field 'left_count'."""
        return self._left_count

    @left_count.setter
    def left_count(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'left_count' field must be of type 'int'"
            assert value >= -9223372036854775808 and value < 9223372036854775808, \
                "The 'left_count' field must be an integer in [-9223372036854775808, 9223372036854775807]"
        self._left_count = value

    @builtins.property
    def right_count(self):
        """Message field 'right_count'."""
        return self._right_count

    @right_count.setter
    def right_count(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'right_count' field must be of type 'int'"
            assert value >= -9223372036854775808 and value < 9223372036854775808, \
                "The 'right_count' field must be an integer in [-9223372036854775808, 9223372036854775807]"
        self._right_count = value

    @builtins.property
    def left_vel(self):
        """Message field 'left_vel'."""
        return self._left_vel

    @left_vel.setter
    def left_vel(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'left_vel' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'left_vel' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._left_vel = value

    @builtins.property
    def right_vel(self):
        """Message field 'right_vel'."""
        return self._right_vel

    @right_vel.setter
    def right_vel(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'right_vel' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'right_vel' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._right_vel = value
