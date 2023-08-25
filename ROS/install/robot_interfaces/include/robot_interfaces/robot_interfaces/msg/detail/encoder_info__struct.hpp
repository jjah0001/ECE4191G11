// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_interfaces:msg/EncoderInfo.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__ENCODER_INFO__STRUCT_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__ENCODER_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_interfaces__msg__EncoderInfo __attribute__((deprecated))
#else
# define DEPRECATED__robot_interfaces__msg__EncoderInfo __declspec(deprecated)
#endif

namespace robot_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct EncoderInfo_
{
  using Type = EncoderInfo_<ContainerAllocator>;

  explicit EncoderInfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_count = 0ll;
      this->right_count = 0ll;
      this->left_vel = 0.0;
      this->right_vel = 0.0;
    }
  }

  explicit EncoderInfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_count = 0ll;
      this->right_count = 0ll;
      this->left_vel = 0.0;
      this->right_vel = 0.0;
    }
  }

  // field types and members
  using _left_count_type =
    int64_t;
  _left_count_type left_count;
  using _right_count_type =
    int64_t;
  _right_count_type right_count;
  using _left_vel_type =
    double;
  _left_vel_type left_vel;
  using _right_vel_type =
    double;
  _right_vel_type right_vel;

  // setters for named parameter idiom
  Type & set__left_count(
    const int64_t & _arg)
  {
    this->left_count = _arg;
    return *this;
  }
  Type & set__right_count(
    const int64_t & _arg)
  {
    this->right_count = _arg;
    return *this;
  }
  Type & set__left_vel(
    const double & _arg)
  {
    this->left_vel = _arg;
    return *this;
  }
  Type & set__right_vel(
    const double & _arg)
  {
    this->right_vel = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_interfaces::msg::EncoderInfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interfaces::msg::EncoderInfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interfaces::msg::EncoderInfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interfaces::msg::EncoderInfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::EncoderInfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::EncoderInfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::EncoderInfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::EncoderInfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interfaces::msg::EncoderInfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interfaces::msg::EncoderInfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interfaces__msg__EncoderInfo
    std::shared_ptr<robot_interfaces::msg::EncoderInfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interfaces__msg__EncoderInfo
    std::shared_ptr<robot_interfaces::msg::EncoderInfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EncoderInfo_ & other) const
  {
    if (this->left_count != other.left_count) {
      return false;
    }
    if (this->right_count != other.right_count) {
      return false;
    }
    if (this->left_vel != other.left_vel) {
      return false;
    }
    if (this->right_vel != other.right_vel) {
      return false;
    }
    return true;
  }
  bool operator!=(const EncoderInfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EncoderInfo_

// alias to use template instance with default allocator
using EncoderInfo =
  robot_interfaces::msg::EncoderInfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__ENCODER_INFO__STRUCT_HPP_
