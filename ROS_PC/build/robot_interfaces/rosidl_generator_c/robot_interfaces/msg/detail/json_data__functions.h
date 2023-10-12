// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from robot_interfaces:msg/JSONData.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__JSON_DATA__FUNCTIONS_H_
#define ROBOT_INTERFACES__MSG__DETAIL__JSON_DATA__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "robot_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "robot_interfaces/msg/detail/json_data__struct.h"

/// Initialize msg/JSONData message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * robot_interfaces__msg__JSONData
 * )) before or use
 * robot_interfaces__msg__JSONData__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
bool
robot_interfaces__msg__JSONData__init(robot_interfaces__msg__JSONData * msg);

/// Finalize msg/JSONData message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
void
robot_interfaces__msg__JSONData__fini(robot_interfaces__msg__JSONData * msg);

/// Create msg/JSONData message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * robot_interfaces__msg__JSONData__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
robot_interfaces__msg__JSONData *
robot_interfaces__msg__JSONData__create();

/// Destroy msg/JSONData message.
/**
 * It calls
 * robot_interfaces__msg__JSONData__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
void
robot_interfaces__msg__JSONData__destroy(robot_interfaces__msg__JSONData * msg);

/// Check for msg/JSONData message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
bool
robot_interfaces__msg__JSONData__are_equal(const robot_interfaces__msg__JSONData * lhs, const robot_interfaces__msg__JSONData * rhs);

/// Copy a msg/JSONData message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
bool
robot_interfaces__msg__JSONData__copy(
  const robot_interfaces__msg__JSONData * input,
  robot_interfaces__msg__JSONData * output);

/// Initialize array of msg/JSONData messages.
/**
 * It allocates the memory for the number of elements and calls
 * robot_interfaces__msg__JSONData__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
bool
robot_interfaces__msg__JSONData__Sequence__init(robot_interfaces__msg__JSONData__Sequence * array, size_t size);

/// Finalize array of msg/JSONData messages.
/**
 * It calls
 * robot_interfaces__msg__JSONData__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
void
robot_interfaces__msg__JSONData__Sequence__fini(robot_interfaces__msg__JSONData__Sequence * array);

/// Create array of msg/JSONData messages.
/**
 * It allocates the memory for the array and calls
 * robot_interfaces__msg__JSONData__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
robot_interfaces__msg__JSONData__Sequence *
robot_interfaces__msg__JSONData__Sequence__create(size_t size);

/// Destroy array of msg/JSONData messages.
/**
 * It calls
 * robot_interfaces__msg__JSONData__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
void
robot_interfaces__msg__JSONData__Sequence__destroy(robot_interfaces__msg__JSONData__Sequence * array);

/// Check for msg/JSONData message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
bool
robot_interfaces__msg__JSONData__Sequence__are_equal(const robot_interfaces__msg__JSONData__Sequence * lhs, const robot_interfaces__msg__JSONData__Sequence * rhs);

/// Copy an array of msg/JSONData messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_interfaces
bool
robot_interfaces__msg__JSONData__Sequence__copy(
  const robot_interfaces__msg__JSONData__Sequence * input,
  robot_interfaces__msg__JSONData__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_INTERFACES__MSG__DETAIL__JSON_DATA__FUNCTIONS_H_
