__author__ = 'canerten'

import urllib2, time, random, json

import helpers
import robotic
import camera

import os.path
import camera_streamer
import tornado
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

cameraStreamer = None

class MainHandler(RequestHandler):
    def get(self):
        print "served index"
        self.render('index.html')


class CameraHandler(RequestHandler):
    def get(self):
        cameraStreamer.startStreaming()


handlers = [
    (r"/", MainHandler),
    (r'/websocket', robotic.RobotHandler),
]

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
)

application = Application(handlers, **settings)
cameraStreamer = camera_streamer.CameraStreamer()


if __name__ == "__main__":
    application.listen(8000)
    cameraStreamerPeriodicCallback = tornado.ioloop.PeriodicCallback(
        cameraStreamer.update, 1000, io_loop=IOLoop.instance())
    cameraStreamerPeriodicCallback.start()

    IOLoop.instance().start()