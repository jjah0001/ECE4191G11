// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_interfaces:msg/Waypoint.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__WAYPOINT__STRUCT_H_
#define ROBOT_INTERFACES__MSG__DETAIL__WAYPOINT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Waypoint in the package robot_interfaces.
typedef struct robot_interfaces__msg__Waypoint
{
  double x;
  double y;
} robot_interfaces__msg__Waypoint;

// Struct for a sequence of robot_interfaces__msg__Waypoint.
typedef struct robot_interfaces__msg__Waypoint__Sequence
{
  robot_interfaces__msg__Waypoint * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interfaces__msg__Waypoint__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_INTERFACES__MSG__DETAIL__WAYPOINT__STRUCT_H_
