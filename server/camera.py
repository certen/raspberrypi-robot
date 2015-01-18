__author__ = 'canerten'
import picamera

def capturePhoto() :
     with picamera.PiCamera() as camera:
    #   camera = picamera.PiCamera()
    #    filename = dt.datetime.now().strftime('static/%Y%m%d-%H%M%S.jpg')

        filename = 'static/picture.jpg'
        camera.capture(filename)
        camera.close
        camera = None
        return filename
