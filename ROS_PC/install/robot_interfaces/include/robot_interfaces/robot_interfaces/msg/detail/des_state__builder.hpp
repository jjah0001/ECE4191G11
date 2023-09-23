// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/DesState.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__DES_STATE__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__DES_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/des_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_DesState_y
{
public:
  explicit Init_DesState_y(::robot_interfaces::msg::DesState & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::DesState y(::robot_interfaces::msg::DesState::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::DesState msg_;
};

class Init_DesState_x
{
public:
  explicit Init_DesState_x(::robot_interfaces::msg::DesState & msg)
  : msg_(msg)
  {}
  Init_DesState_y x(::robot_interfaces::msg::DesState::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_DesState_y(msg_);
  }

private:
  ::robot_interfaces::msg::DesState msg_;
};

class Init_DesState_state
{
public:
  Init_DesState_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DesState_x state(::robot_interfaces::msg::DesState::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_DesState_x(msg_);
  }

private:
  ::robot_interfaces::msg::DesState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::DesState>()
{
  return robot_interfaces::msg::builder::Init_DesState_state();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__DES_STATE__BUILDER_HPP_
