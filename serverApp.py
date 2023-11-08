from flask import Response, Flask
import cv2

app = Flask(__name__)

def gen_frames():

    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if success:
            buffer = cv2.imencode(".jpg", frame)[1]
            stringData = buffer.tostring()
            yield (
                b"--frame\r\n"
                b"Content-Type: text/plain\r\n\r\n" + stringData + b"\r\n"
            )
        else:
            break


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)