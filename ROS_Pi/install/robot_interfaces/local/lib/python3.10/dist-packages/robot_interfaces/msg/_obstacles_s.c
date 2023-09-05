// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from robot_interfaces:msg/Obstacles.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "robot_interfaces/msg/detail/obstacles__struct.h"
#include "robot_interfaces/msg/detail/obstacles__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool robot_interfaces__msg__obstacles__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[42];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("robot_interfaces.msg._obstacles.Obstacles", full_classname_dest, 41) == 0);
  }
  robot_interfaces__msg__Obstacles * ros_message = _ros_message;
  {  // flag
    PyObject * field = PyObject_GetAttrString(_pymsg, "flag");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->flag = (Py_True == field);
    Py_DECREF(field);
  }
  {  // obs1_x
    PyObject * field = PyObject_GetAttrString(_pymsg, "obs1_x");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->obs1_x = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // obs1_y
    PyObject * field = PyObject_GetAttrString(_pymsg, "obs1_y");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->obs1_y = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // obs1_r
    PyObject * field = PyObject_GetAttrString(_pymsg, "obs1_r");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->obs1_r = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // obs2_x
    PyObject * field = PyObject_GetAttrString(_pymsg, "obs2_x");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->obs2_x = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // obs2_y
    PyObject * field = PyObject_GetAttrString(_pymsg, "obs2_y");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->obs2_y = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // obs2_r
    PyObject * field = PyObject_GetAttrString(_pymsg, "obs2_r");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->obs2_r = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * robot_interfaces__msg__obstacles__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Obstacles */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("robot_interfaces.msg._obstacles");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Obstacles");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  robot_interfaces__msg__Obstacles * ros_message = (robot_interfaces__msg__Obstacles *)raw_ros_message;
  {  // flag
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->flag ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "flag", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // obs1_x
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->obs1_x);
    {
      int rc = PyObject_SetAttrString(_pymessage, "obs1_x", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // obs1_y
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->obs1_y);
    {
      int rc = PyObject_SetAttrString(_pymessage, "obs1_y", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // obs1_r
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->obs1_r);
    {
      int rc = PyObject_SetAttrString(_pymessage, "obs1_r", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // obs2_x
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->obs2_x);
    {
      int rc = PyObject_SetAttrString(_pymessage, "obs2_x", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // obs2_y
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->obs2_y);
    {
      int rc = PyObject_SetAttrString(_pymessage, "obs2_y", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // obs2_r
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->obs2_r);
    {
      int rc = PyObject_SetAttrString(_pymessage, "obs2_r", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
