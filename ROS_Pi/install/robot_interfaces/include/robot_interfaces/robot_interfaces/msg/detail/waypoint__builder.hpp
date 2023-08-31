// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/Waypoint.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__WAYPOINT__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__WAYPOINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/waypoint__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_Waypoint_y
{
public:
  explicit Init_Waypoint_y(::robot_interfaces::msg::Waypoint & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::Waypoint y(::robot_interfaces::msg::Waypoint::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::Waypoint msg_;
};

class Init_Waypoint_x
{
public:
  Init_Waypoint_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Waypoint_y x(::robot_interfaces::msg::Waypoint::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Waypoint_y(msg_);
  }

private:
  ::robot_interfaces::msg::Waypoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::Waypoint>()
{
  return robot_interfaces::msg::builder::Init_Waypoint_x();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__WAYPOINT__BUILDER_HPP_
