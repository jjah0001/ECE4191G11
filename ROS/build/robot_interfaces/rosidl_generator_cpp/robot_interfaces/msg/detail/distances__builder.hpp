// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/Distances.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__DISTANCES__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__DISTANCES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/distances__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_Distances_sensor3
{
public:
  explicit Init_Distances_sensor3(::robot_interfaces::msg::Distances & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::Distances sensor3(::robot_interfaces::msg::Distances::_sensor3_type arg)
  {
    msg_.sensor3 = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::Distances msg_;
};

class Init_Distances_sensor2
{
public:
  explicit Init_Distances_sensor2(::robot_interfaces::msg::Distances & msg)
  : msg_(msg)
  {}
  Init_Distances_sensor3 sensor2(::robot_interfaces::msg::Distances::_sensor2_type arg)
  {
    msg_.sensor2 = std::move(arg);
    return Init_Distances_sensor3(msg_);
  }

private:
  ::robot_interfaces::msg::Distances msg_;
};

class Init_Distances_sensor1
{
public:
  Init_Distances_sensor1()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Distances_sensor2 sensor1(::robot_interfaces::msg::Distances::_sensor1_type arg)
  {
    msg_.sensor1 = std::move(arg);
    return Init_Distances_sensor2(msg_);
  }

private:
  ::robot_interfaces::msg::Distances msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::Distances>()
{
  return robot_interfaces::msg::builder::Init_Distances_sensor1();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__DISTANCES__BUILDER_HPP_
