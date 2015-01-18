import copy
import os
import os.path
import subprocess
import time
import logging

# ---------------------------------------------------------------------------------------------------
class CameraStreamer:
    DEFAULT_TIMEOUT = 4.0

    #-----------------------------------------------------------------------------------------------
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self.streamingStartTime = 0
        self.cameraStreamerProcess = None
        self.streamingTimeout = timeout

    #-----------------------------------------------------------------------------------------------
    def __del__(self):
        self.stopStreaming()

    #-----------------------------------------------------------------------------------------------
    def startStreaming(self):

        # Start raspberry_pi_camera_streamer if needed
        if self.cameraStreamerProcess is None:
            self.cameraStreamerProcess = subprocess.Popen(["/home/pi/skynet/start_stream.sh"])

        self.streamingStartTime = time.time()

        #-----------------------------------------------------------------------------------------------

    def update(self):
        if time.time() - self.streamingStartTime > self.streamingTimeout:
            ()
            #  self.stopStreaming()

    #-----------------------------------------------------------------------------------------------
    def stopStreaming(self):
        if self.cameraStreamerProcess is not None:
            subprocess.Popen(
                ["/home/pi/skynet/stop_stream.sh"])
            self.cameraStreamerProcess = None

