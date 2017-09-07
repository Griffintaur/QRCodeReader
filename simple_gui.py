import os, threading, webbrowser
from flask import Flask, request, render_template, Response
from Imagehandler import Imagehandler

app = Flask(__name__, static_folder='Input')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

dest = []

def gen(destination):
    import cv2
    obj = Imagehandler(str(destination))
    TransformImage = obj.QRCodeInImage()
    ret, frame = cv2.imencode('.jpg', TransformImage)
    frame = frame.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/image_feed')
def image_feed():
    return Response(gen(dest[0]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'Input/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
        
    dest.append(destination)
    

    return render_template("complete.html", image_name=filename)

if __name__ == "__main__":
    url = 'http://127.0.0.1:{0}'.format(5000)
    threading.Timer(1.25, lambda : webbrowser.open(url)).start()
    app.run(port=5000, debug=False)
