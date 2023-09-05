// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_interfaces:msg/Obstacles.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__STRUCT_H_
#define ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Obstacles in the package robot_interfaces.
typedef struct robot_interfaces__msg__Obstacles
{
  bool flag;
  double obs1_x;
  double obs1_y;
  double obs1_r;
  double obs2_x;
  double obs2_y;
  double obs2_r;
} robot_interfaces__msg__Obstacles;

// Struct for a sequence of robot_interfaces__msg__Obstacles.
typedef struct robot_interfaces__msg__Obstacles__Sequence
{
  robot_interfaces__msg__Obstacles * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interfaces__msg__Obstacles__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_INTERFACES__MSG__DETAIL__OBSTACLES__STRUCT_H_
