import flask
from flask import Flask, request, render_template, redirect, url_for
import os
import PIL
from PIL import Image
from cv2 import cv2
import face_recognition as fr
import time 

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def verification():
    profile_image = fr.load_image_file('static/images/image.jpeg')
    profile_encoding = fr.face_encodings(profile_image)[0]
    status=[]
    video = cv2.VideoCapture(0)
    t0 = time.time()
    
    while video.isOpened():
        check , frame = video.read()
        
        cv2.imshow('frame',frame)
    
        img = Image.fromarray(frame, 'RGB')
        img.save('static/images/my.jpeg')
    
        live_image = fr.load_image_file('static/images/my.jpeg')
        live_encoding = fr.face_encodings(live_image)[0]
        
        results = fr.compare_faces([profile_encoding],live_encoding)
        status.append(results)
        
        cv2.waitKey(200)
        t1 = time.time()    
      
        if t1-t0 >= 3:
            video.release()
            cv2.destroyAllWindows()
            
    return status

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
     
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = 'image.jpeg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output = verification()
            #print(output)
            if output[0][0] == True:
                return render_template("img.html")
               
            else:
                return redirect(url_for('home'))
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug = True)