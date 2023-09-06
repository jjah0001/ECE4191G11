// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/Pose.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__POSE__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_Pose_theta
{
public:
  explicit Init_Pose_theta(::robot_interfaces::msg::Pose & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::Pose theta(::robot_interfaces::msg::Pose::_theta_type arg)
  {
    msg_.theta = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::Pose msg_;
};

class Init_Pose_y
{
public:
  explicit Init_Pose_y(::robot_interfaces::msg::Pose & msg)
  : msg_(msg)
  {}
  Init_Pose_theta y(::robot_interfaces::msg::Pose::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Pose_theta(msg_);
  }

private:
  ::robot_interfaces::msg::Pose msg_;
};

class Init_Pose_x
{
public:
  Init_Pose_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Pose_y x(::robot_interfaces::msg::Pose::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Pose_y(msg_);
  }

private:
  ::robot_interfaces::msg::Pose msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::Pose>()
{
  return robot_interfaces::msg::builder::Init_Pose_x();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__POSE__BUILDER_HPP_
