#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
) 
from PyQt5.QtCore import Qt
import os

app = QApplication([])
window = QWidget()
window.resize(1440, 680)
window.setWindowTitle('EasyEditor')
lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
dir_files = QListWidget()

btn_contour = QPushButton('Контур')
btn_blur = QPushButton('Размытие')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(dir_files)
col2.addWidget(lb_image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_blur)
row_tools.addWidget(btn_contour)
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
window.setLayout(row)

window.show()

workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.png', '.jpeg', '.bmp', '.jfif']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    dir_files.clear()
    for filename in filenames:
        dir_files.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadImage(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_contour(self):
        self.image = self.image.filter(CONTOUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_blur(self):
        self.image = self.image.filter(BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

workimage = ImageProcessor()

def showChosenImage():
    if dir_files.currentRow() >= 0:
        filename = dir_files.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))

workimage = ImageProcessor()
dir_files.currentRowChanged.connect(showChosenImage)

btn_contour.clicked.connect(workimage.do_contour)
btn_blur.clicked.connect(workimage.do_blur)
btn_left.clicked.connect(workimage.do_left)          
btn_right.clicked.connect(workimage.do_right)       
btn_flip.clicked.connect(workimage.do_flip)            
btn_sharp.clicked.connect(workimage.do_sharpen)       
btn_bw.clicked.connect(workimage.do_bw)          

app.exec()



