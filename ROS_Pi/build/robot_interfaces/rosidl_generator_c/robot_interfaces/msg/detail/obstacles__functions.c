// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robot_interfaces:msg/Obstacles.idl
// generated code does not contain a copyright notice
#include "robot_interfaces/msg/detail/obstacles__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
robot_interfaces__msg__Obstacles__init(robot_interfaces__msg__Obstacles * msg)
{
  if (!msg) {
    return false;
  }
  // flag
  // obs1_x
  // obs1_y
  // obs1_r
  // obs2_x
  // obs2_y
  // obs2_r
  // obs3_x
  // obs3_y
  // obs3_r
  return true;
}

void
robot_interfaces__msg__Obstacles__fini(robot_interfaces__msg__Obstacles * msg)
{
  if (!msg) {
    return;
  }
  // flag
  // obs1_x
  // obs1_y
  // obs1_r
  // obs2_x
  // obs2_y
  // obs2_r
  // obs3_x
  // obs3_y
  // obs3_r
}

bool
robot_interfaces__msg__Obstacles__are_equal(const robot_interfaces__msg__Obstacles * lhs, const robot_interfaces__msg__Obstacles * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // flag
  if (lhs->flag != rhs->flag) {
    return false;
  }
  // obs1_x
  if (lhs->obs1_x != rhs->obs1_x) {
    return false;
  }
  // obs1_y
  if (lhs->obs1_y != rhs->obs1_y) {
    return false;
  }
  // obs1_r
  if (lhs->obs1_r != rhs->obs1_r) {
    return false;
  }
  // obs2_x
  if (lhs->obs2_x != rhs->obs2_x) {
    return false;
  }
  // obs2_y
  if (lhs->obs2_y != rhs->obs2_y) {
    return false;
  }
  // obs2_r
  if (lhs->obs2_r != rhs->obs2_r) {
    return false;
  }
  // obs3_x
  if (lhs->obs3_x != rhs->obs3_x) {
    return false;
  }
  // obs3_y
  if (lhs->obs3_y != rhs->obs3_y) {
    return false;
  }
  // obs3_r
  if (lhs->obs3_r != rhs->obs3_r) {
    return false;
  }
  return true;
}

bool
robot_interfaces__msg__Obstacles__copy(
  const robot_interfaces__msg__Obstacles * input,
  robot_interfaces__msg__Obstacles * output)
{
  if (!input || !output) {
    return false;
  }
  // flag
  output->flag = input->flag;
  // obs1_x
  output->obs1_x = input->obs1_x;
  // obs1_y
  output->obs1_y = input->obs1_y;
  // obs1_r
  output->obs1_r = input->obs1_r;
  // obs2_x
  output->obs2_x = input->obs2_x;
  // obs2_y
  output->obs2_y = input->obs2_y;
  // obs2_r
  output->obs2_r = input->obs2_r;
  // obs3_x
  output->obs3_x = input->obs3_x;
  // obs3_y
  output->obs3_y = input->obs3_y;
  // obs3_r
  output->obs3_r = input->obs3_r;
  return true;
}

robot_interfaces__msg__Obstacles *
robot_interfaces__msg__Obstacles__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_interfaces__msg__Obstacles * msg = (robot_interfaces__msg__Obstacles *)allocator.allocate(sizeof(robot_interfaces__msg__Obstacles), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robot_interfaces__msg__Obstacles));
  bool success = robot_interfaces__msg__Obstacles__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robot_interfaces__msg__Obstacles__destroy(robot_interfaces__msg__Obstacles * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robot_interfaces__msg__Obstacles__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robot_interfaces__msg__Obstacles__Sequence__init(robot_interfaces__msg__Obstacles__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_interfaces__msg__Obstacles * data = NULL;

  if (size) {
    data = (robot_interfaces__msg__Obstacles *)allocator.zero_allocate(size, sizeof(robot_interfaces__msg__Obstacles), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robot_interfaces__msg__Obstacles__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robot_interfaces__msg__Obstacles__fini(&data[i - 1]);
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
robot_interfaces__msg__Obstacles__Sequence__fini(robot_interfaces__msg__Obstacles__Sequence * array)
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
      robot_interfaces__msg__Obstacles__fini(&array->data[i]);
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

robot_interfaces__msg__Obstacles__Sequence *
robot_interfaces__msg__Obstacles__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_interfaces__msg__Obstacles__Sequence * array = (robot_interfaces__msg__Obstacles__Sequence *)allocator.allocate(sizeof(robot_interfaces__msg__Obstacles__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robot_interfaces__msg__Obstacles__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robot_interfaces__msg__Obstacles__Sequence__destroy(robot_interfaces__msg__Obstacles__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robot_interfaces__msg__Obstacles__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robot_interfaces__msg__Obstacles__Sequence__are_equal(const robot_interfaces__msg__Obstacles__Sequence * lhs, const robot_interfaces__msg__Obstacles__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robot_interfaces__msg__Obstacles__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robot_interfaces__msg__Obstacles__Sequence__copy(
  const robot_interfaces__msg__Obstacles__Sequence * input,
  robot_interfaces__msg__Obstacles__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robot_interfaces__msg__Obstacles);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robot_interfaces__msg__Obstacles * data =
      (robot_interfaces__msg__Obstacles *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robot_interfaces__msg__Obstacles__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robot_interfaces__msg__Obstacles__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robot_interfaces__msg__Obstacles__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
