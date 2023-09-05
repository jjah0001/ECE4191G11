// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/Obstacles.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/obstacles__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_Obstacles_obs3_r
{
public:
  explicit Init_Obstacles_obs3_r(::robot_interfaces::msg::Obstacles & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::Obstacles obs3_r(::robot_interfaces::msg::Obstacles::_obs3_r_type arg)
  {
    msg_.obs3_r = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

class Init_Obstacles_obs3_y
{
public:
  explicit Init_Obstacles_obs3_y(::robot_interfaces::msg::Obstacles & msg)
  : msg_(msg)
  {}
  Init_Obstacles_obs3_r obs3_y(::robot_interfaces::msg::Obstacles::_obs3_y_type arg)
  {
    msg_.obs3_y = std::move(arg);
    return Init_Obstacles_obs3_r(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

class Init_Obstacles_obs3_x
{
public:
  explicit Init_Obstacles_obs3_x(::robot_interfaces::msg::Obstacles & msg)
  : msg_(msg)
  {}
  Init_Obstacles_obs3_y obs3_x(::robot_interfaces::msg::Obstacles::_obs3_x_type arg)
  {
    msg_.obs3_x = std::move(arg);
    return Init_Obstacles_obs3_y(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

class Init_Obstacles_obs2_r
{
public:
  explicit Init_Obstacles_obs2_r(::robot_interfaces::msg::Obstacles & msg)
  : msg_(msg)
  {}
  Init_Obstacles_obs3_x obs2_r(::robot_interfaces::msg::Obstacles::_obs2_r_type arg)
  {
    msg_.obs2_r = std::move(arg);
    return Init_Obstacles_obs3_x(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

class Init_Obstacles_obs2_y
{
public:
  explicit Init_Obstacles_obs2_y(::robot_interfaces::msg::Obstacles & msg)
  : msg_(msg)
  {}
  Init_Obstacles_obs2_r obs2_y(::robot_interfaces::msg::Obstacles::_obs2_y_type arg)
  {
    msg_.obs2_y = std::move(arg);
    return Init_Obstacles_obs2_r(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

class Init_Obstacles_obs2_x
{
public:
  explicit Init_Obstacles_obs2_x(::robot_interfaces::msg::Obstacles & msg)
  : msg_(msg)
  {}
  Init_Obstacles_obs2_y obs2_x(::robot_interfaces::msg::Obstacles::_obs2_x_type arg)
  {
    msg_.obs2_x = std::move(arg);
    return Init_Obstacles_obs2_y(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

class Init_Obstacles_obs1_r
{
public:
  explicit Init_Obstacles_obs1_r(::robot_interfaces::msg::Obstacles & msg)
  : msg_(msg)
  {}
  Init_Obstacles_obs2_x obs1_r(::robot_interfaces::msg::Obstacles::_obs1_r_type arg)
  {
    msg_.obs1_r = std::move(arg);
    return Init_Obstacles_obs2_x(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

class Init_Obstacles_obs1_y
{
public:
  explicit Init_Obstacles_obs1_y(::robot_interfaces::msg::Obstacles & msg)
  : msg_(msg)
  {}
  Init_Obstacles_obs1_r obs1_y(::robot_interfaces::msg::Obstacles::_obs1_y_type arg)
  {
    msg_.obs1_y = std::move(arg);
    return Init_Obstacles_obs1_r(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

class Init_Obstacles_obs1_x
{
public:
  explicit Init_Obstacles_obs1_x(::robot_interfaces::msg::Obstacles & msg)
  : msg_(msg)
  {}
  Init_Obstacles_obs1_y obs1_x(::robot_interfaces::msg::Obstacles::_obs1_x_type arg)
  {
    msg_.obs1_x = std::move(arg);
    return Init_Obstacles_obs1_y(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

class Init_Obstacles_flag
{
public:
  Init_Obstacles_flag()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Obstacles_obs1_x flag(::robot_interfaces::msg::Obstacles::_flag_type arg)
  {
    msg_.flag = std::move(arg);
    return Init_Obstacles_obs1_x(msg_);
  }

private:
  ::robot_interfaces::msg::Obstacles msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::Obstacles>()
{
  return robot_interfaces::msg::builder::Init_Obstacles_flag();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__BUILDER_HPP_
