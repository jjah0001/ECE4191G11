// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robot_interfaces:msg/Obstacles.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__TRAITS_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robot_interfaces/msg/detail/obstacles__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robot_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Obstacles & msg,
  std::ostream & out)
{
  out << "{";
  // member: flag
  {
    out << "flag: ";
    rosidl_generator_traits::value_to_yaml(msg.flag, out);
    out << ", ";
  }

  // member: obs1_x
  {
    out << "obs1_x: ";
    rosidl_generator_traits::value_to_yaml(msg.obs1_x, out);
    out << ", ";
  }

  // member: obs1_y
  {
    out << "obs1_y: ";
    rosidl_generator_traits::value_to_yaml(msg.obs1_y, out);
    out << ", ";
  }

  // member: obs1_r
  {
    out << "obs1_r: ";
    rosidl_generator_traits::value_to_yaml(msg.obs1_r, out);
    out << ", ";
  }

  // member: obs2_x
  {
    out << "obs2_x: ";
    rosidl_generator_traits::value_to_yaml(msg.obs2_x, out);
    out << ", ";
  }

  // member: obs2_y
  {
    out << "obs2_y: ";
    rosidl_generator_traits::value_to_yaml(msg.obs2_y, out);
    out << ", ";
  }

  // member: obs2_r
  {
    out << "obs2_r: ";
    rosidl_generator_traits::value_to_yaml(msg.obs2_r, out);
    out << ", ";
  }

  // member: obs3_x
  {
    out << "obs3_x: ";
    rosidl_generator_traits::value_to_yaml(msg.obs3_x, out);
    out << ", ";
  }

  // member: obs3_y
  {
    out << "obs3_y: ";
    rosidl_generator_traits::value_to_yaml(msg.obs3_y, out);
    out << ", ";
  }

  // member: obs3_r
  {
    out << "obs3_r: ";
    rosidl_generator_traits::value_to_yaml(msg.obs3_r, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Obstacles & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: flag
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "flag: ";
    rosidl_generator_traits::value_to_yaml(msg.flag, out);
    out << "\n";
  }

  // member: obs1_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obs1_x: ";
    rosidl_generator_traits::value_to_yaml(msg.obs1_x, out);
    out << "\n";
  }

  // member: obs1_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obs1_y: ";
    rosidl_generator_traits::value_to_yaml(msg.obs1_y, out);
    out << "\n";
  }

  // member: obs1_r
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obs1_r: ";
    rosidl_generator_traits::value_to_yaml(msg.obs1_r, out);
    out << "\n";
  }

  // member: obs2_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obs2_x: ";
    rosidl_generator_traits::value_to_yaml(msg.obs2_x, out);
    out << "\n";
  }

  // member: obs2_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obs2_y: ";
    rosidl_generator_traits::value_to_yaml(msg.obs2_y, out);
    out << "\n";
  }

  // member: obs2_r
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obs2_r: ";
    rosidl_generator_traits::value_to_yaml(msg.obs2_r, out);
    out << "\n";
  }

  // member: obs3_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obs3_x: ";
    rosidl_generator_traits::value_to_yaml(msg.obs3_x, out);
    out << "\n";
  }

  // member: obs3_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obs3_y: ";
    rosidl_generator_traits::value_to_yaml(msg.obs3_y, out);
    out << "\n";
  }

  // member: obs3_r
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obs3_r: ";
    rosidl_generator_traits::value_to_yaml(msg.obs3_r, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Obstacles & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace robot_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use robot_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robot_interfaces::msg::Obstacles & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const robot_interfaces::msg::Obstacles & msg)
{
  return robot_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robot_interfaces::msg::Obstacles>()
{
  return "robot_interfaces::msg::Obstacles";
}

template<>
inline const char * name<robot_interfaces::msg::Obstacles>()
{
  return "robot_interfaces/msg/Obstacles";
}

template<>
struct has_fixed_size<robot_interfaces::msg::Obstacles>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robot_interfaces::msg::Obstacles>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robot_interfaces::msg::Obstacles>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__TRAITS_HPP_
