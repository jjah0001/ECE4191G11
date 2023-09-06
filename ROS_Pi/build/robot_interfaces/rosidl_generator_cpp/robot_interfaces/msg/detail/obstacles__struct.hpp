// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_interfaces:msg/Obstacles.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__STRUCT_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_interfaces__msg__Obstacles __attribute__((deprecated))
#else
# define DEPRECATED__robot_interfaces__msg__Obstacles __declspec(deprecated)
#endif

namespace robot_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Obstacles_
{
  using Type = Obstacles_<ContainerAllocator>;

  explicit Obstacles_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->flag = false;
      this->obs1_x = 0.0;
      this->obs1_y = 0.0;
      this->obs1_r = 0.0;
      this->obs2_x = 0.0;
      this->obs2_y = 0.0;
      this->obs2_r = 0.0;
      this->obs3_x = 0.0;
      this->obs3_y = 0.0;
      this->obs3_r = 0.0;
    }
  }

  explicit Obstacles_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->flag = false;
      this->obs1_x = 0.0;
      this->obs1_y = 0.0;
      this->obs1_r = 0.0;
      this->obs2_x = 0.0;
      this->obs2_y = 0.0;
      this->obs2_r = 0.0;
      this->obs3_x = 0.0;
      this->obs3_y = 0.0;
      this->obs3_r = 0.0;
    }
  }

  // field types and members
  using _flag_type =
    bool;
  _flag_type flag;
  using _obs1_x_type =
    double;
  _obs1_x_type obs1_x;
  using _obs1_y_type =
    double;
  _obs1_y_type obs1_y;
  using _obs1_r_type =
    double;
  _obs1_r_type obs1_r;
  using _obs2_x_type =
    double;
  _obs2_x_type obs2_x;
  using _obs2_y_type =
    double;
  _obs2_y_type obs2_y;
  using _obs2_r_type =
    double;
  _obs2_r_type obs2_r;
  using _obs3_x_type =
    double;
  _obs3_x_type obs3_x;
  using _obs3_y_type =
    double;
  _obs3_y_type obs3_y;
  using _obs3_r_type =
    double;
  _obs3_r_type obs3_r;

  // setters for named parameter idiom
  Type & set__flag(
    const bool & _arg)
  {
    this->flag = _arg;
    return *this;
  }
  Type & set__obs1_x(
    const double & _arg)
  {
    this->obs1_x = _arg;
    return *this;
  }
  Type & set__obs1_y(
    const double & _arg)
  {
    this->obs1_y = _arg;
    return *this;
  }
  Type & set__obs1_r(
    const double & _arg)
  {
    this->obs1_r = _arg;
    return *this;
  }
  Type & set__obs2_x(
    const double & _arg)
  {
    this->obs2_x = _arg;
    return *this;
  }
  Type & set__obs2_y(
    const double & _arg)
  {
    this->obs2_y = _arg;
    return *this;
  }
  Type & set__obs2_r(
    const double & _arg)
  {
    this->obs2_r = _arg;
    return *this;
  }
  Type & set__obs3_x(
    const double & _arg)
  {
    this->obs3_x = _arg;
    return *this;
  }
  Type & set__obs3_y(
    const double & _arg)
  {
    this->obs3_y = _arg;
    return *this;
  }
  Type & set__obs3_r(
    const double & _arg)
  {
    this->obs3_r = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_interfaces::msg::Obstacles_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interfaces::msg::Obstacles_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interfaces::msg::Obstacles_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interfaces::msg::Obstacles_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::Obstacles_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::Obstacles_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::Obstacles_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::Obstacles_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interfaces::msg::Obstacles_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interfaces::msg::Obstacles_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interfaces__msg__Obstacles
    std::shared_ptr<robot_interfaces::msg::Obstacles_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interfaces__msg__Obstacles
    std::shared_ptr<robot_interfaces::msg::Obstacles_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Obstacles_ & other) const
  {
    if (this->flag != other.flag) {
      return false;
    }
    if (this->obs1_x != other.obs1_x) {
      return false;
    }
    if (this->obs1_y != other.obs1_y) {
      return false;
    }
    if (this->obs1_r != other.obs1_r) {
      return false;
    }
    if (this->obs2_x != other.obs2_x) {
      return false;
    }
    if (this->obs2_y != other.obs2_y) {
      return false;
    }
    if (this->obs2_r != other.obs2_r) {
      return false;
    }
    if (this->obs3_x != other.obs3_x) {
      return false;
    }
    if (this->obs3_y != other.obs3_y) {
      return false;
    }
    if (this->obs3_r != other.obs3_r) {
      return false;
    }
    return true;
  }
  bool operator!=(const Obstacles_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Obstacles_

// alias to use template instance with default allocator
using Obstacles =
  robot_interfaces::msg::Obstacles_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__STRUCT_HPP_
