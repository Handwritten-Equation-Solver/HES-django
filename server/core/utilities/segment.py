import cv2
import numpy as np
import os.path
import math


ymin,ymax,xmax,xmin = 0,0,0,0
xminCrop, yminCrop = 100000, 100000
xmaxCrop, ymaxCrop = 0, 0


def img_segment(file):
    
    global ymax,ymin,xmax,xmin
    
    print("Segmenting " + file + "...")
    path=os.path.join("media",file)
    im = cv2.imread(path)
    global gray_image
    gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    folder_path,name = os.path.split(path)
    folder_path = os.path.splitext(folder_path)[0]
    print("Folder Path " + folder_path)

    gray_path = os.path.join(folder_path, "gray_"+name)
    print("Storing grayscale to.."+gray_path)
    
    im = gray_image
    mini = 255
    maxi = 0  
    j=0
    while j < im.shape[1]:
        i=0
        while i<im.shape[0]:
            if im[i][j] > maxi:
                maxi = im[i][j]
            if im[i][j] < mini:
                mini = im[i][j]
            i = i +1
        j = j + 1
    avg = (maxi + mini)/2
    j=0
    while j < im.shape[1]:
        i=0
        while i<im.shape[0]:
            if im[i][j] <avg:
                im[i][j] = 0
            else:
                im[i][j] = 255
            i = i+1
        j = j+1

    

    gray_image = im
    
    cv2.imwrite(gray_path, gray_image)    

    segmented_image_list = []
    flag = 0
    write_flag = False
    global output_image
    output_image = np.full((gray_image.shape[0], gray_image.shape[1]), 255)

    print("conversion done")

    j=0
    while j < gray_image.shape[1]:
        i=0
        while i<gray_image.shape[0]:

            if gray_image[i][j] <= 123:
                write_flag = True

                # yjump,xmax,xmin = 
                yjump = dfs(i,j)

                global xminCrop, xmaxCrop, yminCrop, ymaxCrop
                xminCrop = min(xminCrop, xmin)
                yminCrop = min(yminCrop, ymin)
                xmaxCrop = max(xmaxCrop, xmax)
                ymaxCrop = max(ymaxCrop, ymax)

                max_jump = int(yjump*0.5)
                if max_jump != 0: #And symbol is not square root -> Has to be dealt seperately
                    j += max_jump
                    i=-1


            i+=1
        j+=1

        if write_flag:
            print("reached write_flag")
            write_flag = False
            flag += 1
            print("Storing seg" + str(flag))
            print("x : ",ymin,ymax)
            print("y : ",xmin,xmax)
            
            seg_path = os.path.join(folder_path,str(flag)+"seg_"+ name)
            output_image = output_image[xminCrop:xmaxCrop, yminCrop:ymaxCrop]

            ydiff = xmax-xmin
            xdiff = ymax-ymin
            # pads each side with 50 pixels
            pad1 = 20
            pad2 = 20

            if xdiff>ydiff:
                pad1 += (xdiff-ydiff)/2
            else:
                pad2 += (ydiff-xdiff)/2

            output_image = cv2.copyMakeBorder(output_image,
                    math.floor(pad1),math.ceil(pad1),math.floor(pad2),math.ceil(pad2),
                    cv2.BORDER_CONSTANT,value=[255,255,255])

            cv2.imwrite(seg_path,output_image)            
            output_image = np.full((gray_image.shape[0], gray_image.shape[1]), 255)
            segmented_image_list.append(seg_path)

            xminCrop, yminCrop = 100000, 100000
            xmaxCrop, ymaxCrop = 0, 0

    return segmented_image_list

def dfs(a,b):
#Iterative
    global ymax,ymin,xmax,xmin
    ymin,ymax = b,b
    xmax,xmin = a,a

    stack = []
    stack.append((a, b))
    while len(stack):
        x = stack[-1][0]
        y = stack[-1][1]

        # if ymax < y:
        #     ymax = y
        ymax = max(y, ymax)
        ymin = min(y, ymin)

        xmax = max(x, xmax)
        xmin = min(x, xmin)

        stack.pop()

        if gray_image[x][y] > 123:
            continue
        else:
            gray_image[x][y] = 255
            output_image[x][y] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if i+x>=0 and i+x<gray_image.shape[0] and y+j>=0 and y+j<gray_image.shape[1] :
                        stack.append((x+i,y+j))
    return (ymax-ymin)