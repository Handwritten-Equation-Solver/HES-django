import os
import pickle
directory = "/home/student26/HES_data/train" 
#fill this is in using the pwd command in the ssh shell, give FULL path


L = []
for folder in os.scandir(directory):
	L.append(str(folder.name))


pickle.dump(L, open("mapping.txt", "wb"))

#using pickle.load to open this file and assign it to a list
# Remember to use the file more "rb" while opening, it stands for "read binary"

