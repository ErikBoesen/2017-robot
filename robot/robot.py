#!/usr/bin/env python3

import magicbot
import wpilib

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from networktables.util import ntproperty

from robotpy_ext.common_drivers import navx

from networktables.networktable import NetworkTable

from components import shooter


class MyRobot(magicbot.MagicRobot):

    shooter = shooter.Shooter

    def createObjects(self):
        """Create basic components (motor controllers, joysticks, etc.)"""
        # NavX (purple board on top of the RoboRIO)
        self.navX = navx.AHRS.create_spi()

        # Initialize SmartDashboard
        self.sd = NetworkTable.getTable('SmartDashboard')

        # Joysticks
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        # Motors
        # TODO: Drive Motors

        self.shooter_motor = wpilib.CANTalon(5)

        # TODO: Drivetrain object

    def autonomous(self):
        """Prepare for autonomous mode"""
        pass

    def disabledPeriodic(self):
        """Repeat periodically while robot is disabled. Usually emptied.
        Sometimes used to easily test sensors and other things."""
        pass

    def disabledInit(self):
        """Do once right away when robot is disabled."""

    def teleopInit(self):
        """Do when teleoperated mode is started."""

    def teleopPeriodic(self):
        """Do periodically while robot is in teleoperated mode."""
        # Temporary: Spin shooter motor based on joystick1's Y.
        self.shooter.rpm = self.joystick1.getY() * 1024

if __name__ == '__main__':
    wpilib.run(MyRobot)
