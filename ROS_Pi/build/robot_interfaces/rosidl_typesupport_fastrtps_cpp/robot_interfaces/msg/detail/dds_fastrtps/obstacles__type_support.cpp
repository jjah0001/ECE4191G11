// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from robot_interfaces:msg/Obstacles.idl
// generated code does not contain a copyright notice
#include "robot_interfaces/msg/detail/obstacles__rosidl_typesupport_fastrtps_cpp.hpp"
#include "robot_interfaces/msg/detail/obstacles__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace robot_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robot_interfaces
cdr_serialize(
  const robot_interfaces::msg::Obstacles & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: flag
  cdr << (ros_message.flag ? true : false);
  // Member: obs1_x
  cdr << ros_message.obs1_x;
  // Member: obs1_y
  cdr << ros_message.obs1_y;
  // Member: obs1_r
  cdr << ros_message.obs1_r;
  // Member: obs2_x
  cdr << ros_message.obs2_x;
  // Member: obs2_y
  cdr << ros_message.obs2_y;
  // Member: obs2_r
  cdr << ros_message.obs2_r;
  // Member: obs3_x
  cdr << ros_message.obs3_x;
  // Member: obs3_y
  cdr << ros_message.obs3_y;
  // Member: obs3_r
  cdr << ros_message.obs3_r;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robot_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  robot_interfaces::msg::Obstacles & ros_message)
{
  // Member: flag
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.flag = tmp ? true : false;
  }

  // Member: obs1_x
  cdr >> ros_message.obs1_x;

  // Member: obs1_y
  cdr >> ros_message.obs1_y;

  // Member: obs1_r
  cdr >> ros_message.obs1_r;

  // Member: obs2_x
  cdr >> ros_message.obs2_x;

  // Member: obs2_y
  cdr >> ros_message.obs2_y;

  // Member: obs2_r
  cdr >> ros_message.obs2_r;

  // Member: obs3_x
  cdr >> ros_message.obs3_x;

  // Member: obs3_y
  cdr >> ros_message.obs3_y;

  // Member: obs3_r
  cdr >> ros_message.obs3_r;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robot_interfaces
get_serialized_size(
  const robot_interfaces::msg::Obstacles & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: flag
  {
    size_t item_size = sizeof(ros_message.flag);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obs1_x
  {
    size_t item_size = sizeof(ros_message.obs1_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obs1_y
  {
    size_t item_size = sizeof(ros_message.obs1_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obs1_r
  {
    size_t item_size = sizeof(ros_message.obs1_r);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obs2_x
  {
    size_t item_size = sizeof(ros_message.obs2_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obs2_y
  {
    size_t item_size = sizeof(ros_message.obs2_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obs2_r
  {
    size_t item_size = sizeof(ros_message.obs2_r);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obs3_x
  {
    size_t item_size = sizeof(ros_message.obs3_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obs3_y
  {
    size_t item_size = sizeof(ros_message.obs3_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: obs3_r
  {
    size_t item_size = sizeof(ros_message.obs3_r);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robot_interfaces
max_serialized_size_Obstacles(
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


  // Member: flag
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: obs1_x
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: obs1_y
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: obs1_r
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: obs2_x
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: obs2_y
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: obs2_r
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: obs3_x
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: obs3_y
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: obs3_r
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  return current_alignment - initial_alignment;
}

static bool _Obstacles__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const robot_interfaces::msg::Obstacles *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Obstacles__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<robot_interfaces::msg::Obstacles *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Obstacles__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const robot_interfaces::msg::Obstacles *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Obstacles__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Obstacles(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Obstacles__callbacks = {
  "robot_interfaces::msg",
  "Obstacles",
  _Obstacles__cdr_serialize,
  _Obstacles__cdr_deserialize,
  _Obstacles__get_serialized_size,
  _Obstacles__max_serialized_size
};

static rosidl_message_type_support_t _Obstacles__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Obstacles__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace robot_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_robot_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<robot_interfaces::msg::Obstacles>()
{
  return &robot_interfaces::msg::typesupport_fastrtps_cpp::_Obstacles__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robot_interfaces, msg, Obstacles)() {
  return &robot_interfaces::msg::typesupport_fastrtps_cpp::_Obstacles__handle;
}

#ifdef __cplusplus
}
#endif
