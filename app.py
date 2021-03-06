import sys
if sys.platform == 'linux':
	import Xlib.threaded
else:
	import Xlib.threaded
from flask import Flask, render_template, Response, request
from camera_desktop import Camera

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
	return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
	app.run(host='127.0.0.1', threaded=True)
