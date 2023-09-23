# Zerynth - libs - nxp-mag3110/mag3110.py
#
# Zerynth library for MAG3110 digital sensor
#
# @Author: Stefano Torneo
#
# @Date: 2020-08-24
# @Last Modified by: 
# @Last Modified time:

"""
.. module:: MAG3110

**************
MAG3110 Module
**************

.. _datasheet: https://www.nxp.com/docs/en/data-sheet/MAG3110.pdf

This module contains the Zerynth driver for MAG3110 digital sensor. 
It features a standard I2C serial interface output and smart embedded
functions.
The MAG3110 is capable of measuring magnetic fields with an output data rate
(ODR) up to 80 Hz; these output data rates correspond to sample intervals from
12.5 ms to several seconds.

"""

import i2c

# two's complement
#
# @param      v      integer value to be converted
# @param      n_bit  number of bits of v's representation
#
# @return     the two's complement of v
#
def _tc(v, n_bit=16):
    mask = 2**(n_bit - 1)
    return -(v & mask) + (v & ~mask)

# Define some constants from the datasheet

DR_STATUS = 0x00
CTRL_REG1 = 0x10
CTRL_REG2 = 0X11
OUT_X_MSB = 0x01
OUT_X_LSB = 0x02 
OUT_Y_MSB = 0x03
OUT_Y_LSB = 0x04
OUT_Z_MSB = 0x05
OUT_Z_LSB = 0x06
DIE_TEMP = 0x0F
WHO_AM_I_REG = 0x07
SYSMOD_REG = 0x08
ACTIVE_MODE = 0x01
OFF_X_MSB = 0x09
OFF_Y_MSB = 0x0B
OFF_Z_MSB = 0x0D

class MAG3110(i2c.I2C):
    """
    
===============
 MAG3110 class
===============

.. class:: MAG3110(drvname, addr=0x0E, clk=400000)

    Creates an intance of the MAG3110 class.

    :param drvname: I2C Bus used '( I2C0, ... )'
    :param addr: Slave address, default 0x0E
    :param clk: Clock speed, default 400kHz
    
    Magnetometer values can be easily obtained from the sensor: ::

        from nxp.mag3110 import mag3110

        ...

        mag = mag3110.MAG3110(I2C0)

        mag_values = mag.get_values()

    """
    
    # dictionary for axis
    axis = {
        'X': OFF_X_MSB,
        'Y': OFF_Y_MSB,
        'Z': OFF_Z_MSB
    }

    # dictionary for oversampling rate
    osr = {
      '16': 0,
      '32': 1,
      '64': 2,
      '128': 3  
    } 

    def __init__(self, drvname, addr=0x0E, clk=400000):
        
        if (addr != 0x0E):
            raise ValueError

        i2c.I2C.__init__(self,drvname,addr,clk)
        try:
            self.start()
        except PeripheralError as e:
            print(e)

        if (self.write_read(WHO_AM_I_REG, n=1)[0] != 0xC4): 
            raise ValueError
        
        # Reset value of CTRL registers
        self.set_mode(0) # set standby mode to write register CTRL_REG1
        self.write_bytes(CTRL_REG1, 0x00)
        self.write_bytes(CTRL_REG2, 0x00)
       
        # Set some configurations
        self.set_offset_on()
        self.set_offset("X", 0)
        self.set_offset("Y", 0)
        self.set_offset("Z", 0)
        self.set_offset_temp()
        self.set_measurement()

    ##
    ## @brief      Set the value of the register in the position indicated, according to the param new_val.
    ##
    ## @param      self
    ## @param      reg  is the reg where to write.
    ## @param      pos  is the position of register where to write.
    ## @param      state    boolean value to set the value of the register in the position indicated.
    ## @return     nothing
    ##
    def write_register_bit(self, reg, pos, new_val):
        if (pos < 0):
            raise ValueError

        if (new_val < 0):
            raise ValueError

        value = self.write_read(reg, n=1)[0]
        value |= (new_val << pos)
        self.write_bytes(reg, value)
        value = self.write_read(reg, n=1)[0]

    def set_measurement(self, mode=0, osr=32, odr=1):
        """
    
    .. method:: set_measurement(mode = 0, osr = 32, odr = 1)

        **Parameters**:
        
        **mode**: is the measurement mode to set (default value = 0). Values accepted: 0 or 1.

        ======== ====================
         mode       Measurement mode
        ======== ====================
         0        Continuous measurements
         1        Triggered measurements
        ======== ====================

        **osr**: is oversampling rate to set (default value = 32). Values accepted: 16, 32, 64 or 128.

        **odr**: is output data rate to set (default value = 1). Values range accepted: 0-7.

        Set the measurement mode, the oversampling rate and output data rate.

        """
        if (mode != 0 and mode != 1):
            raise ValueError

        if (osr not in [16, 32, 64, 128]):
            raise ValueError
    
        if (odr < 0 or odr > 7):
            raise ValueError
        
        self.set_mode(0) # set standby mode

        self.write_register_bit(CTRL_REG1, 1, mode) # set measurement mode

        # get osr value from dictionary
        osr_value = self.osr[str(osr)]

        self.write_register_bit(CTRL_REG1, 3, osr_value) # set osr
        self.write_register_bit(CTRL_REG1, 5, odr) # set odr

        # Enable Auto Mag Reset
        self.write_register_bit(CTRL_REG2, 7, 1)

        # if continous measurement mode
        if (mode == 0): 
            self.set_mode(1) # set active mode

    def set_mode(self, mode):
        """
    
    .. method:: set_mode(mode)

       **Parameters**:

       **mode**: is the operation mode to set. Values accepted: 0 or 1.

       ======== ====================
         mode       Operating mode
       ======== ====================
         0         Standby mode
         1         Active mode
       ======== ====================

       Set the operating mode.

        """
        if (mode != 0 and mode != 1):
            raise ValueError

        if (mode == 0):
            current = self.write_read(CTRL_REG1, n=1)[0]
	        # Clear bits 0 and 1 to enter low power standby mode
            self.write_bytes(CTRL_REG1, (current & ~(0x3)))
        else:
            current = self.write_read(CTRL_REG1, n=1)[0]
            self.write_bytes(CTRL_REG1, (current | ACTIVE_MODE))
    
    def set_offset_on(self):
        """

    .. method:: set_offset_on()

        Enable the correction of data values according to offset register values.

        """
        value = self.write_read(CTRL_REG2, n=1)[0]
        value &= ~(1 << 5)
        self.write_bytes(CTRL_REG2, value)
    
    def set_offset_off(self):
        """

    .. method:: set_offset_off()

        Disable the correction of data values according to offset register values.

        """
        value = self.write_read(CTRL_REG2, n=1)[0]
        value |= (1 << 5)
        self.write_bytes(CTRL_REG2, value)
    
    def set_offset(self, axis, offset):
        """

    .. method:: set_offset(axis, offset)

        :param axis: is the axis to set. Values accepted: "X", "Y" or "Z".
        :param offset: is the offset to set to the axis indicated. Values range accepted: [-10000, 10000].

        Set offset to the axis specified.

        """
        if (axis not in ["X", "Y", "Z"]):
            raise ValueError

        if (offset > 10000 or offset < -10000):
            raise ValueError

        # get register of axis from dictionary
        reg_axis = self.axis[axis]
        # correct the offset value
        offset = -(offset) << 1
        # write on msb address 
        self.write_bytes(reg_axis, ((offset >> 8) & 0xFF))
        sleep(15)
        # write on lsb address
        self.write_bytes(reg_axis + 1, offset & 0xFF)

    def is_data_ready(self):
        """

    .. method:: is_data_ready()
        
        Return 1 if new data ready, otherwise 0.

        """
        status = self.write_read(DR_STATUS, n=1)[0]
        return (status & 0x8) >> 3
    
    # It is not recommended for applications that require high accuracy, especially with low over-sampling settings.
    def trigger_measurement(self):
        """

    .. method:: trigger_measurement()

        Set measurement in trigger mode.

        """
        current = self.write_read(CTRL_REG1, n=1)[0]
        self.write_bytes(CTRL_REG1, (current | 0x02))

    def get_values(self):
        """

    .. method:: get_values()

        Return the X, Y and Z values of the magnetometer in a dictionary.

        """
        # Read 6 bytes from register 0x01
        # X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
        data = self.write_read(OUT_X_MSB, n=6)
    
        # Convert data
        xMag = _tc(data[0] * 256 + data[1])
        yMag = _tc(data[2] * 256 + data[3])
        zMag = _tc(data[4] * 256 + data[5])
        value = self.write_read(CTRL_REG2, n=1)[0]

        return {'x': xMag, 'y': yMag, 'z': zMag}
    
    def set_offset_temp(self, value=10):
        """

    .. method:: set_offset_temp(value = 10)

        :param value: is the value of temperature offset to set. Default value is 10.

        Set the offset value of temperature.

        """
        self.offset_temp = value

    def get_temp(self):
        """

    .. method:: get_temp()

        Return the temperature in degrees Celsius.

        """
        # The temperature sensor offset is not factory trimmed and must be calibrated by the user software if higher absolute accuracy is required. 
        # Note: The register allows for temperature measurements from -128°C to 127°C but the output range is limited to -40°C to 125°C.

        raw_temp = self.write_read(DIE_TEMP, n=1)[0]

        return _tc(raw_temp, n_bit=8) + self.offset_temp
