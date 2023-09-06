// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_interfaces:msg/Final.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__FINAL__STRUCT_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__FINAL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_interfaces__msg__Final __attribute__((deprecated))
#else
# define DEPRECATED__robot_interfaces__msg__Final __declspec(deprecated)
#endif

namespace robot_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Final_
{
  using Type = Final_<ContainerAllocator>;

  explicit Final_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->flag = false;
    }
  }

  explicit Final_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->flag = false;
    }
  }

  // field types and members
  using _flag_type =
    bool;
  _flag_type flag;

  // setters for named parameter idiom
  Type & set__flag(
    const bool & _arg)
  {
    this->flag = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_interfaces::msg::Final_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interfaces::msg::Final_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interfaces::msg::Final_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interfaces::msg::Final_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::Final_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::Final_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::Final_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::Final_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interfaces::msg::Final_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interfaces::msg::Final_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interfaces__msg__Final
    std::shared_ptr<robot_interfaces::msg::Final_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interfaces__msg__Final
    std::shared_ptr<robot_interfaces::msg::Final_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Final_ & other) const
  {
    if (this->flag != other.flag) {
      return false;
    }
    return true;
  }
  bool operator!=(const Final_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Final_

// alias to use template instance with default allocator
using Final =
  robot_interfaces::msg::Final_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__FINAL__STRUCT_HPP_
