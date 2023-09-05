# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robot_interfaces:msg/Obstacles.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Obstacles(type):
    """Metaclass of message 'Obstacles'."""

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
                'robot_interfaces.msg.Obstacles')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__obstacles
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__obstacles
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__obstacles
            cls._TYPE_SUPPORT = module.type_support_msg__msg__obstacles
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__obstacles

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Obstacles(metaclass=Metaclass_Obstacles):
    """Message class 'Obstacles'."""

    __slots__ = [
        '_flag',
        '_obs1_x',
        '_obs1_y',
        '_obs1_r',
        '_obs2_x',
        '_obs2_y',
        '_obs2_r',
        '_obs3_x',
        '_obs3_y',
        '_obs3_r',
    ]

    _fields_and_field_types = {
        'flag': 'boolean',
        'obs1_x': 'double',
        'obs1_y': 'double',
        'obs1_r': 'double',
        'obs2_x': 'double',
        'obs2_y': 'double',
        'obs2_r': 'double',
        'obs3_x': 'double',
        'obs3_y': 'double',
        'obs3_r': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.flag = kwargs.get('flag', bool())
        self.obs1_x = kwargs.get('obs1_x', float())
        self.obs1_y = kwargs.get('obs1_y', float())
        self.obs1_r = kwargs.get('obs1_r', float())
        self.obs2_x = kwargs.get('obs2_x', float())
        self.obs2_y = kwargs.get('obs2_y', float())
        self.obs2_r = kwargs.get('obs2_r', float())
        self.obs3_x = kwargs.get('obs3_x', float())
        self.obs3_y = kwargs.get('obs3_y', float())
        self.obs3_r = kwargs.get('obs3_r', float())

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
        if self.flag != other.flag:
            return False
        if self.obs1_x != other.obs1_x:
            return False
        if self.obs1_y != other.obs1_y:
            return False
        if self.obs1_r != other.obs1_r:
            return False
        if self.obs2_x != other.obs2_x:
            return False
        if self.obs2_y != other.obs2_y:
            return False
        if self.obs2_r != other.obs2_r:
            return False
        if self.obs3_x != other.obs3_x:
            return False
        if self.obs3_y != other.obs3_y:
            return False
        if self.obs3_r != other.obs3_r:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def flag(self):
        """Message field 'flag'."""
        return self._flag

    @flag.setter
    def flag(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'flag' field must be of type 'bool'"
        self._flag = value

    @builtins.property
    def obs1_x(self):
        """Message field 'obs1_x'."""
        return self._obs1_x

    @obs1_x.setter
    def obs1_x(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obs1_x' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'obs1_x' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._obs1_x = value

    @builtins.property
    def obs1_y(self):
        """Message field 'obs1_y'."""
        return self._obs1_y

    @obs1_y.setter
    def obs1_y(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obs1_y' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'obs1_y' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._obs1_y = value

    @builtins.property
    def obs1_r(self):
        """Message field 'obs1_r'."""
        return self._obs1_r

    @obs1_r.setter
    def obs1_r(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obs1_r' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'obs1_r' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._obs1_r = value

    @builtins.property
    def obs2_x(self):
        """Message field 'obs2_x'."""
        return self._obs2_x

    @obs2_x.setter
    def obs2_x(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obs2_x' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'obs2_x' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._obs2_x = value

    @builtins.property
    def obs2_y(self):
        """Message field 'obs2_y'."""
        return self._obs2_y

    @obs2_y.setter
    def obs2_y(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obs2_y' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'obs2_y' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._obs2_y = value

    @builtins.property
    def obs2_r(self):
        """Message field 'obs2_r'."""
        return self._obs2_r

    @obs2_r.setter
    def obs2_r(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obs2_r' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'obs2_r' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._obs2_r = value

    @builtins.property
    def obs3_x(self):
        """Message field 'obs3_x'."""
        return self._obs3_x

    @obs3_x.setter
    def obs3_x(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obs3_x' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'obs3_x' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._obs3_x = value

    @builtins.property
    def obs3_y(self):
        """Message field 'obs3_y'."""
        return self._obs3_y

    @obs3_y.setter
    def obs3_y(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obs3_y' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'obs3_y' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._obs3_y = value

    @builtins.property
    def obs3_r(self):
        """Message field 'obs3_r'."""
        return self._obs3_r

    @obs3_r.setter
    def obs3_r(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'obs3_r' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'obs3_r' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._obs3_r = value
