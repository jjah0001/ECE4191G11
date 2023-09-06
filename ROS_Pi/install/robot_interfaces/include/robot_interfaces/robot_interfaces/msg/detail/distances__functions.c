// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robot_interfaces:msg/Distances.idl
// generated code does not contain a copyright notice
#include "robot_interfaces/msg/detail/distances__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
robot_interfaces__msg__Distances__init(robot_interfaces__msg__Distances * msg)
{
  if (!msg) {
    return false;
  }
  // sensor1
  // sensor2
  // sensor3
  return true;
}

void
robot_interfaces__msg__Distances__fini(robot_interfaces__msg__Distances * msg)
{
  if (!msg) {
    return;
  }
  // sensor1
  // sensor2
  // sensor3
}

bool
robot_interfaces__msg__Distances__are_equal(const robot_interfaces__msg__Distances * lhs, const robot_interfaces__msg__Distances * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // sensor1
  if (lhs->sensor1 != rhs->sensor1) {
    return false;
  }
  // sensor2
  if (lhs->sensor2 != rhs->sensor2) {
    return false;
  }
  // sensor3
  if (lhs->sensor3 != rhs->sensor3) {
    return false;
  }
  return true;
}

bool
robot_interfaces__msg__Distances__copy(
  const robot_interfaces__msg__Distances * input,
  robot_interfaces__msg__Distances * output)
{
  if (!input || !output) {
    return false;
  }
  // sensor1
  output->sensor1 = input->sensor1;
  // sensor2
  output->sensor2 = input->sensor2;
  // sensor3
  output->sensor3 = input->sensor3;
  return true;
}

robot_interfaces__msg__Distances *
robot_interfaces__msg__Distances__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_interfaces__msg__Distances * msg = (robot_interfaces__msg__Distances *)allocator.allocate(sizeof(robot_interfaces__msg__Distances), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robot_interfaces__msg__Distances));
  bool success = robot_interfaces__msg__Distances__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robot_interfaces__msg__Distances__destroy(robot_interfaces__msg__Distances * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robot_interfaces__msg__Distances__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robot_interfaces__msg__Distances__Sequence__init(robot_interfaces__msg__Distances__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_interfaces__msg__Distances * data = NULL;

  if (size) {
    data = (robot_interfaces__msg__Distances *)allocator.zero_allocate(size, sizeof(robot_interfaces__msg__Distances), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robot_interfaces__msg__Distances__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robot_interfaces__msg__Distances__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
robot_interfaces__msg__Distances__Sequence__fini(robot_interfaces__msg__Distances__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      robot_interfaces__msg__Distances__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

robot_interfaces__msg__Distances__Sequence *
robot_interfaces__msg__Distances__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_interfaces__msg__Distances__Sequence * array = (robot_interfaces__msg__Distances__Sequence *)allocator.allocate(sizeof(robot_interfaces__msg__Distances__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robot_interfaces__msg__Distances__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robot_interfaces__msg__Distances__Sequence__destroy(robot_interfaces__msg__Distances__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robot_interfaces__msg__Distances__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robot_interfaces__msg__Distances__Sequence__are_equal(const robot_interfaces__msg__Distances__Sequence * lhs, const robot_interfaces__msg__Distances__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robot_interfaces__msg__Distances__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robot_interfaces__msg__Distances__Sequence__copy(
  const robot_interfaces__msg__Distances__Sequence * input,
  robot_interfaces__msg__Distances__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robot_interfaces__msg__Distances);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robot_interfaces__msg__Distances * data =
      (robot_interfaces__msg__Distances *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robot_interfaces__msg__Distances__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robot_interfaces__msg__Distances__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robot_interfaces__msg__Distances__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
