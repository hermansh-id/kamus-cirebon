import os, sys
from pdf2image import convert_from_path
path_this = os.path.abspath(os.path.dirname(__file__))
path_compressed = os.path.join(path_this, "compressed_file")

def convertpdf(path_root, name, target):
    pages = convert_from_path(os.path.join(path_root, name))
    list_file = []
    for i in range(len(pages)):
        print(i)
        save_dir = os.path.join(target, name + '_' + str(i) +'.jpg')
        list_file.append(save_dir)
        pages[i].save(save_dir, 'JPEG')
    return list_file



convertpdf(path_this, "kamus.pdf", path_compressed)
