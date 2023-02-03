from PIL import Image
import os
path_this = os.path.abspath(os.path.dirname(__file__))
path_compressed = os.path.join(path_this, "compressed_file")

i = 1
for root, dirs, files in os.walk(path_compressed, topdown=False):
    for name in files:
        img = Image.open(os.path.join(path_compressed, name))
        w, h = img.size
        img.crop((0, 0, w/2, h)).save(os.path.join(path_this, 'jpg', str(i) + '.jpg'))
        i = i+1
        img.crop((w/2, 0, w, h)).save(os.path.join(path_this, 'jpg', str(i) + '.jpg'))
        i = i+1