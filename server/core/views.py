from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .utilities.segment import img_segment
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

        #Segment Image here
        segmented_image_list = img_segment(file)
        #Returns list of paths of segmented images

        # TODO [x]: In segment.py store min and max y co-ordinate of each segment to compare with other algos
        print(segmented_image_list)

        # TODO []: Integrate Recognizer module

        
        # TODO []: JSON array with image_path,prediction,min,max
        # TODO []: Algorithm to parse equation in format need by MATH engine
        # TODO []: Pass to Math Engine
        # TODO []: Delete the media/<eqn> folder

        return render(request, 'core/home.html', {
            'uploaded_file_url': path
            #TODO [] : Return solutions
        })

    return render(request, 'core/home.html')