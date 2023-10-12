// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_interfaces:msg/JSONData.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__JSON_DATA__STRUCT_H_
#define ROBOT_INTERFACES__MSG__DETAIL__JSON_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'json_data'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/JSONData in the package robot_interfaces.
typedef struct robot_interfaces__msg__JSONData
{
  rosidl_runtime_c__String json_data;
} robot_interfaces__msg__JSONData;

// Struct for a sequence of robot_interfaces__msg__JSONData.
typedef struct robot_interfaces__msg__JSONData__Sequence
{
  robot_interfaces__msg__JSONData * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interfaces__msg__JSONData__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_INTERFACES__MSG__DETAIL__JSON_DATA__STRUCT_H_
