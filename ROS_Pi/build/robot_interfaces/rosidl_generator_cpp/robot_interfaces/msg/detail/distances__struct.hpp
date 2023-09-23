// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_interfaces:msg/Distances.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__DISTANCES__STRUCT_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__DISTANCES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_interfaces__msg__Distances __attribute__((deprecated))
#else
# define DEPRECATED__robot_interfaces__msg__Distances __declspec(deprecated)
#endif

namespace robot_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Distances_
{
  using Type = Distances_<ContainerAllocator>;

  explicit Distances_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sensor1 = 0.0;
      this->sensor2 = 0.0;
      this->sensor3 = 0.0;
    }
  }

  explicit Distances_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sensor1 = 0.0;
      this->sensor2 = 0.0;
      this->sensor3 = 0.0;
    }
  }

  // field types and members
  using _sensor1_type =
    double;
  _sensor1_type sensor1;
  using _sensor2_type =
    double;
  _sensor2_type sensor2;
  using _sensor3_type =
    double;
  _sensor3_type sensor3;

  // setters for named parameter idiom
  Type & set__sensor1(
    const double & _arg)
  {
    this->sensor1 = _arg;
    return *this;
  }
  Type & set__sensor2(
    const double & _arg)
  {
    this->sensor2 = _arg;
    return *this;
  }
  Type & set__sensor3(
    const double & _arg)
  {
    this->sensor3 = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_interfaces::msg::Distances_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interfaces::msg::Distances_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interfaces::msg::Distances_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interfaces::msg::Distances_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::Distances_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::Distances_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::Distances_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::Distances_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interfaces::msg::Distances_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interfaces::msg::Distances_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interfaces__msg__Distances
    std::shared_ptr<robot_interfaces::msg::Distances_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interfaces__msg__Distances
    std::shared_ptr<robot_interfaces::msg::Distances_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Distances_ & other) const
  {
    if (this->sensor1 != other.sensor1) {
      return false;
    }
    if (this->sensor2 != other.sensor2) {
      return false;
    }
    if (this->sensor3 != other.sensor3) {
      return false;
    }
    return true;
  }
  bool operator!=(const Distances_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Distances_

// alias to use template instance with default allocator
using Distances =
  robot_interfaces::msg::Distances_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__DISTANCES__STRUCT_HPP_
