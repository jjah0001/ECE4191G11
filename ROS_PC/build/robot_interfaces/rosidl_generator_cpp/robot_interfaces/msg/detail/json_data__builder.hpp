// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/JSONData.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__JSON_DATA__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__JSON_DATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/json_data__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_JSONData_json_data
{
public:
  Init_JSONData_json_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_interfaces::msg::JSONData json_data(::robot_interfaces::msg::JSONData::_json_data_type arg)
  {
    msg_.json_data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::JSONData msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::JSONData>()
{
  return robot_interfaces::msg::builder::Init_JSONData_json_data();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__JSON_DATA__BUILDER_HPP_
