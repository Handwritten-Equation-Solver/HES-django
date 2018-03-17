import cv2
import numpy as np
import os.path
import math


ymin,ymax,xmax,xmin = 0,0,0,0

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
    cv2.imwrite(gray_path, gray_image)
    segmented_image_list = []
    flag = 0
    write_flag = False
    global output_image
    output_image = np.full((gray_image.shape[0], gray_image.shape[1]), 255)

    j=0
    while j < gray_image.shape[1]:
        i=0
        while i<gray_image.shape[0]:

            if gray_image[i][j] <= 123:
                write_flag = True

                # yjump,xmax,xmin = 
                yjump = dfs(i,j)
                max_jump = int(yjump*0.5)
                if max_jump != 0: #And symbol is not square root -> Has to be dealt seperately
                    j += max_jump
                    i=-1


            i+=1
        j+=1

        if write_flag:
            write_flag = False
            flag += 1
            print("Storing seg" + str(flag))
            print("x : ",ymin,ymax)
            print("y : ",xmin,xmax)
            
            seg_path = os.path.join(folder_path,str(flag)+"seg_"+ name)
            output_image = output_image[xmin:xmax, ymin:ymax]

            xdiff = xmax-xmin
            ydiff = ymax-ymin

            pad1 = 50 # pads each side with 50 pixels
            pad2 = 50

            if xdiff>ydiff:
                pad1 += xdiff-ydiff
            else:
                pad2 += ydiff-xdiff;

            output_image = cv2.copyMakeBorder(output_image,pad1,pad1,pad2,pad2,cv2.BORDER_CONSTANT,value=[255,255,255])
            cv2.imwrite(seg_path,output_image)            
            output_image = np.full((gray_image.shape[0], gray_image.shape[1]), 255)
            segmented_image_list.append(seg_path)

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
