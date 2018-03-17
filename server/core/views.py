from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .utilities.segment import img_segment
from .utilities.keras_model.predict import predict_image
# from sympy.solvers import solve #Sympy math solver
import os.path

# Load template
def home(request):
    return render(request, 'core/home.html') #without context info

#POST request to send image to server
def home(request):
    # Check if a file is sent
    if request.method == 'POST' and request.FILES['img']:
        
        img = request.FILES['img']
        fs = FileSystemStorage()
        foldername = img.name.split(".")[0]

        #a.jpg will be stored in media/a/a.jpg
        file = fs.save(os.path.join(foldername,img.name), img)
        print(file + " Received")
        #uploaded_file_url = fs.url(file)
        path = os.path.join("media",file)

        #Returns list of square segmented image paths
        segmented_image_list = img_segment(file)
        print(segmented_image_list)

        predicted_list = []
        #Print the recognised character
        for img in segmented_image_list:
            predicted_list.append(predict_image(img))

        # TODO []: Pass predicted list to solver.py
        # TODO []: Delete the media/<eqn> folder

        return render(request, 'core/home.html', {
            'uploaded_file_url': path
            #TODO [] : Return solutions
        })

    return render(request, 'core/home.html')