#!/usr/bin/env python3
import wpilib
from networktables import NetworkTables
from comms.com import Comm
from actions.drive import Drive
from actions.arm import Arm
from sensors.ultrasonic import Ultrasconic_Sensor
from sensors.switch import Switch
from control.toggle import Toggle
from control.bool import Logic

class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.table = NetworkTables.getTable("SmartDashboard")
        self.robot_drive = wpilib.RobotDrive(0,1)
        self.stick = wpilib.Joystick(0)
        self.climbingMotor = wpilib.Talon(2)
        self.gearSwitch1 = wpilib.DigitalInput(0)
        self.gearSwitch2 = wpilib.DigitalInput(1)
        self.gearSwitch3 = wpilib.DigitalInput(2)
        self.gearSwitch4 = wpilib.DigitalInput(3)
        self.ballSwitch1 = wpilib.DigitalInput(4)
        self.ballSwitch2 = wpilib.DigitalInput(5)
        self.gearMotor1 = wpilib.Spark(4)
        self.gearMotor2 = wpilib.Spark(3)
        self.ballMotor1 = wpilib.Relay(0)
        self.gyro = wpilib.ADXRS450_Gyro(0)
        self.gearSpeed = .5
        self.lights = wpilib.Relay(1)
        self.lightToggle = False
        self.lightToggleBool = True
        self.togglev = 0
        wpilib.CameraServer.launch()
        self.ultrasonic = wpilib.AnalogInput(0)


    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.auto_loop_counter = 0

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""


    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        if self.stick.getRawButton(5):
            if self.togglev == 0:
                self.robot_drive.arcadeDrive(-0.75*self.stick.getY(), self.table.getNumber("cameraX", 0)/1.6)
                self.togglev = 1
            else:
                self.robot_drive.arcadeDrive(-0.75*self.stick.getY(), self.table.getNumber("cameraX", 0)*1.4)
                self.togglev = 0
        elif self.stick.getRawButton(9):
            self.robot_drive.arcadeDrive(-1*self.stick.getY(),-1*self.stick.getX())
        else:
            self.robot_drive.arcadeDrive(-0.75*self.stick.getY(),-0.75*self.stick.getX())




        if self.stick.getRawButton(3):
            self.climbingMotor.set(-.3)
        else:
            self.climbingMotor.set(0)

        if self.stick.getRawButton(4) and self.lightToggleBool == False:
            pass
        elif self.stick.getRawButton(4) and self.lightToggleBool:
            self.lightToggle = not self.lightToggle
            if self.lightToggle:
                self.lights.set(wpilib.Relay.Value.kForward)
            else:
                self.lights.set(wpilib.Relay.Value.kOff)
            self.lightToggleBool = False
        elif self.stick.getRawButton(4) == False and self.lightToggleBool == False:
            self.lightToggleBool = True



        if self.stick.getRawButton(1) and self.gearSwitch2.get()== False:
            self.gearMotor1.set(0)
        elif self.stick.getRawButton(1) and self.gearSwitch2.get():
            self.gearMotor1.set(.5)
        elif self.stick.getRawButton(1) == False and self.gearSwitch1.get()== False:
            self.gearMotor1.set(0)
        elif self.stick.getRawButton(1) == False and self.gearSwitch1.get():
            self.gearMotor1.set(-.5)


        if self.stick.getRawButton(1) == False and self.gearSwitch3.get()== False:
            self.gearMotor2.set(0)
        elif self.stick.getRawButton(1) == False and self.gearSwitch3.get():
            self.gearMotor2.set(.5)
        elif self.stick.getRawButton(1) and self.gearSwitch4.get()== False:
            self.gearMotor2.set(0)
        elif self.stick.getRawButton(1) and self.gearSwitch4.get():
            self.gearMotor2.set(-.5)

        if self.stick.getRawButton(2) == False and self.ballSwitch1.get()==False:
            self.ballMotor1.set(wpilib.Relay.Value.kOff)
        elif self.stick.getRawButton(2) == False and self.ballSwitch1.get():
            self.ballMotor1.set(wpilib.Relay.Value.kReverse)
        elif self.stick.getRawButton(2) and self.ballSwitch2.get()==False:
            self.ballMotor1.set(wpilib.Relay.Value.kOff)
        elif self.stick.getRawButton(2) and self.ballSwitch2.get():
            self.ballMotor1.set(wpilib.Relay.Value.kForward)

        self.table.putNumber('ultra', self.ultrasonic.getVoltage())
        self.table.putNumber('GearMotor1 Forward', self.gearMotor1.get())
        self.table.putNumber('GearMotor2 Forward', self.gearMotor2.get())
        self.table.putNumber('GearMotor1 Reverse', self.gearMotor1.get())
        self.table.putNumber('GearMotor2 Reverse', self.gearMotor2.get())
        self.table.putNumber('gyro', self.gyro.getAngle())

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
