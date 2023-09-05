// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from robot_interfaces:msg/Obstacles.idl
// generated code does not contain a copyright notice
#include "robot_interfaces/msg/detail/obstacles__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "robot_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "robot_interfaces/msg/detail/obstacles__struct.h"
#include "robot_interfaces/msg/detail/obstacles__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _Obstacles__ros_msg_type = robot_interfaces__msg__Obstacles;

static bool _Obstacles__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Obstacles__ros_msg_type * ros_message = static_cast<const _Obstacles__ros_msg_type *>(untyped_ros_message);
  // Field name: flag
  {
    cdr << (ros_message->flag ? true : false);
  }

  // Field name: obs1_x
  {
    cdr << ros_message->obs1_x;
  }

  // Field name: obs1_y
  {
    cdr << ros_message->obs1_y;
  }

  // Field name: obs1_r
  {
    cdr << ros_message->obs1_r;
  }

  // Field name: obs2_x
  {
    cdr << ros_message->obs2_x;
  }

  // Field name: obs2_y
  {
    cdr << ros_message->obs2_y;
  }

  // Field name: obs2_r
  {
    cdr << ros_message->obs2_r;
  }

  return true;
}

static bool _Obstacles__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Obstacles__ros_msg_type * ros_message = static_cast<_Obstacles__ros_msg_type *>(untyped_ros_message);
  // Field name: flag
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->flag = tmp ? true : false;
  }

  // Field name: obs1_x
  {
    cdr >> ros_message->obs1_x;
  }

  // Field name: obs1_y
  {
    cdr >> ros_message->obs1_y;
  }

  // Field name: obs1_r
  {
    cdr >> ros_message->obs1_r;
  }

  // Field name: obs2_x
  {
    cdr >> ros_message->obs2_x;
  }

  // Field name: obs2_y
  {
    cdr >> ros_message->obs2_y;
  }

  // Field name: obs2_r
  {
    cdr >> ros_message->obs2_r;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_robot_interfaces
size_t get_serialized_size_robot_interfaces__msg__Obstacles(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Obstacles__ros_msg_type * ros_message = static_cast<const _Obstacles__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name flag
  {
    size_t item_size = sizeof(ros_message->flag);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name obs1_x
  {
    size_t item_size = sizeof(ros_message->obs1_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name obs1_y
  {
    size_t item_size = sizeof(ros_message->obs1_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name obs1_r
  {
    size_t item_size = sizeof(ros_message->obs1_r);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name obs2_x
  {
    size_t item_size = sizeof(ros_message->obs2_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name obs2_y
  {
    size_t item_size = sizeof(ros_message->obs2_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name obs2_r
  {
    size_t item_size = sizeof(ros_message->obs2_r);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _Obstacles__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_robot_interfaces__msg__Obstacles(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_robot_interfaces
size_t max_serialized_size_robot_interfaces__msg__Obstacles(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: flag
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: obs1_x
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: obs1_y
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: obs1_r
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: obs2_x
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: obs2_y
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: obs2_r
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  return current_alignment - initial_alignment;
}

static size_t _Obstacles__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_robot_interfaces__msg__Obstacles(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Obstacles = {
  "robot_interfaces::msg",
  "Obstacles",
  _Obstacles__cdr_serialize,
  _Obstacles__cdr_deserialize,
  _Obstacles__get_serialized_size,
  _Obstacles__max_serialized_size
};

static rosidl_message_type_support_t _Obstacles__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Obstacles,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, robot_interfaces, msg, Obstacles)() {
  return &_Obstacles__type_support;
}

#if defined(__cplusplus)
}
#endif
