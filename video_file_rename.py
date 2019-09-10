import os
import sys

if sys.argv.__len__() < 2:
    raise Exception("Give me the animation download dir as parameter >_<")

for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        file_name = os.path.splitext(file)[0]
        ext_name = os.path.splitext(file)[1]
        if ext_name == ".mp4":
            pos = file_name.find("_batch")
            if not pos == -1:
                os.rename(os.path.join(root, file), os.path.join(root, file[:pos]+".mp4"))

