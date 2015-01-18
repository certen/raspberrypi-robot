from traceback import format_exc
import tornado

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.escape import json_encode

__author__ = 'canerten'
import PicoBorgRev
import datetime as dt

import time
import os
import sys

import PicoBorgRev


class RobotHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(RobotHandler, self).__init__(*args, **kwargs)

        self.PBR = PicoBorgRev.PicoBorgRev()  # Create a new PicoBorg Reverse object
        self.PBR.Init()  # Set the board up (checks the board is connected)
        self.PBR.ResetEpo()  # Reset the stop switch (EPO) state
        print "robot handler started"
        if not self.PBR.foundChip:
            boards = PicoBorgRev.ScanForPicoBorgReverse()
            if len(boards) == 0:
                print 'No PicoBorg Reverse found, check you are attached :)'
            else:
                print 'No PicoBorg Reverse at address %02X, but we did find boards:' % (self.PBR.i2cAddress)
                for board in boards:
                    print '    %02X (%d)' % (board, board)
                print 'If you need to change the IC address change the setup line so it is correct, e.g.'
                print 'PBR.i2cAddress = 0x%02X' % (boards[0])



        # Settings for the joystick
        axisUpDown = 1  # Joystick axis to read for up / down position
        axisUpDownInverted = False  # Set this to True if up and down appear to be swapped
        axisLeftRight = 2  # Joystick axis to read for left / right position
        axisLeftRightInverted = False  # Set this to True if left and right appear to be swapped
        buttonResetEpo = 3  # Joystick button number to perform an EPO reset (Start)
        buttonSlow = 8  # Joystick button number for driving slowly whilst held (L2)
        slowFactor = 0.5  # Speed to slow to when the drive slowly button is held, e.g. 0.5 would be half speed
        buttonFastTurn = 9  # Joystick button number for turning fast (R2)
        interval = 0.00  # Time between updates in seconds, smaller responds faster but uses more processor time


    # -----------------------------------------------------------------------------------------------
    def __del__(self):
        print "robot handler stopped"
        self.PBR.MotorsOff()
        pass

    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        try:
            print "Message received " + message

            data = tornado.escape.json_decode(message)
            command = data['command']
            if command == "move":
                x, y = data['x'], data['y']
                print "move %f %f" % ( x, y)

                upDown = y / 20.0
                leftRight = x / 20.0

                driveLeft = -upDown
                driveRight = upDown
                print "received x %f y %f" % (leftRight, upDown)
                absconstant = 0.15
                if leftRight < -absconstant:
                    # Turning left
                    if abs(upDown) < absconstant:
                        driveLeft = leftRight
                        driveRight = leftRight
                    else:
                        driveLeft *= 1.0 + (2.0 * leftRight)

                elif leftRight > absconstant:
                    # Turning right
                    if abs(upDown) < absconstant:
                        driveRight = leftRight
                        driveLeft = leftRight
                    else :
                        driveLeft *= 1.0 + (2.0 * leftRight)

                print "set motor %f %f" % ( driveLeft, driveRight)
                self.PBR.SetMotor1(driveLeft)
                self.PBR.SetMotor2(driveRight)
            if command == "stop":
                print "stopped"
                self.PBR.MotorsOff()

            # convert message 0 - 20 to -1 to 1
            # fix message format
            # joystick -10
            # start
            # stop
            # request = {'command':'x', 'value': 4}

            response = {'status': 'success', 'response': None}
            self.write_message(json_encode(response))
        except Exception, e:
            self.PBR.MotorsOff()
            print >> sys.stderr, "Error occured:\n%s" % format_exc()
            errorResponse = {'status': 'fail', 'error': "Error occured:\n%s" % format_exc()}
            self.write_message(json_encode(errorResponse))


    def on_close(self):
        print "WebSocket closed"

    def moveForward(self):
        self.PBR.ResetEpo()
        self.PBR.SetMotor1(0.2)
        self.PBR.SetMotor2(0.2)

    def stop(self):
        self.PBR.ResetEpo()
        self.PBR.SetMotor1(0)
        self.PBR.SetMotor2(0)