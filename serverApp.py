from flask import Flask, Response
import cv2


class EndpointAction(object):

    def __init__(self, action, mimetype="multipart/x-mixed-replace; boundary=frame"): 
        self.action = action
        self.mimetype = mimetype

    def __call__(self, *args):  
        answer = self.action()
        return Response(answer, mimetype=self.mimetype)


class FlaskAppWrapper(object):
    app = None

    def __init__(self, nameServer, host='127.0.0.1', port=5000, debug=False):
        self.app = Flask(nameServer)
        self.host = host
        self.port = port
        self.debug = debug

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))


def stream():

    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if success:
            imgEncode = cv2.imencode(".jpg", frame)[1]
            bytesImgEnconde = imgEncode.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: text/plain\r\n\r\n" + bytesImgEnconde + b"\r\n"
            )
        else:
            break

def get_images():

    while True:

        img = cv2.imread('C:/Users/thiago.santos/Desktop/INV-34600/images/3digit/streamPy/image.png')

        if img is not None:

            imgEncode = cv2.imencode(".jpg", img)[1]
            bytesImgEnconde = imgEncode.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: text/plain\r\n\r\n" + bytesImgEnconde + b"\r\n"
            )

if __name__ == "__main__":
    serverApp = FlaskAppWrapper(__name__, debug=True)
    serverApp.add_endpoint(endpoint="/stream", endpoint_name="stream", handler=stream)
    serverApp.add_endpoint(endpoint="/imgTest", endpoint_name="imgTest", handler=get_images)
    serverApp.run()
