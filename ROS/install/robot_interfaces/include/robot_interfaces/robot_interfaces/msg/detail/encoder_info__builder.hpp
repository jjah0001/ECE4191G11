// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/EncoderInfo.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__ENCODER_INFO__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__ENCODER_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/encoder_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_EncoderInfo_right_vel
{
public:
  explicit Init_EncoderInfo_right_vel(::robot_interfaces::msg::EncoderInfo & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::EncoderInfo right_vel(::robot_interfaces::msg::EncoderInfo::_right_vel_type arg)
  {
    msg_.right_vel = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::EncoderInfo msg_;
};

class Init_EncoderInfo_left_vel
{
public:
  explicit Init_EncoderInfo_left_vel(::robot_interfaces::msg::EncoderInfo & msg)
  : msg_(msg)
  {}
  Init_EncoderInfo_right_vel left_vel(::robot_interfaces::msg::EncoderInfo::_left_vel_type arg)
  {
    msg_.left_vel = std::move(arg);
    return Init_EncoderInfo_right_vel(msg_);
  }

private:
  ::robot_interfaces::msg::EncoderInfo msg_;
};

class Init_EncoderInfo_right_count
{
public:
  explicit Init_EncoderInfo_right_count(::robot_interfaces::msg::EncoderInfo & msg)
  : msg_(msg)
  {}
  Init_EncoderInfo_left_vel right_count(::robot_interfaces::msg::EncoderInfo::_right_count_type arg)
  {
    msg_.right_count = std::move(arg);
    return Init_EncoderInfo_left_vel(msg_);
  }

private:
  ::robot_interfaces::msg::EncoderInfo msg_;
};

class Init_EncoderInfo_left_count
{
public:
  Init_EncoderInfo_left_count()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EncoderInfo_right_count left_count(::robot_interfaces::msg::EncoderInfo::_left_count_type arg)
  {
    msg_.left_count = std::move(arg);
    return Init_EncoderInfo_right_count(msg_);
  }

private:
  ::robot_interfaces::msg::EncoderInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::EncoderInfo>()
{
  return robot_interfaces::msg::builder::Init_EncoderInfo_left_count();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__ENCODER_INFO__BUILDER_HPP_
