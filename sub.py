import os
import platform
import sys
import http

if sys.argv.__len__() < 2:
    raise Exception("Give me the animation download dir as parameter >_<")

def get_font(font_name: str):
    font_path = ""
    
    return font_path