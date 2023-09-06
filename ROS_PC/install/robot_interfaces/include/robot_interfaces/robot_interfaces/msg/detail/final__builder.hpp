// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/Final.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__FINAL__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__FINAL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/final__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_Final_flag
{
public:
  Init_Final_flag()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_interfaces::msg::Final flag(::robot_interfaces::msg::Final::_flag_type arg)
  {
    msg_.flag = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::Final msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::Final>()
{
  return robot_interfaces::msg::builder::Init_Final_flag();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__FINAL__BUILDER_HPP_
