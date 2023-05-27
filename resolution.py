from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import cv2 as cv
import numpy as np
import time
import os

class Resolution(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Make High-Resolution IMG")
        self.setGeometry(400,400,420,200) # 화면에 나타날 윈도우의 위치와 크기를 지정
        
        self.inittext = QLabel("저해상도 이미지를 고해상도로 바꾸어 주는 프로그램", self)
        self.inittext.move(10, 10)
        self.inittext.resize(500, 20)
        
        imgopenButton = QPushButton('이미지 열기', self) # 버튼 생성
        convertButton = QPushButton('이미지 변환', self)
        exportButton = QPushButton('내보내기', self)
        quitButton = QPushButton('나가기', self)
        realtimeButton = QPushButton('Real Time', self)
        
        self.scaletext = QLabel("Scale (2,4,8 만 가능) : ", self)
        self.scaletext.move(10, 73)
        self.scaletext.resize(300, 20)
        
        self.scale = QComboBox(self)
        self.scale.addItems(['2', '4', '8'])
        self.scale.move(165, 70)
        self.scale.activated[str].connect(self.scalepick)
 
        self.radio1 = QRadioButton("Bicubic(고전방법)", self)
        self.method = "bicubic"
        self.radio1.move(10, 100)
        self.radio1.resize(500,20)
        self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.radioButton_clicked) 
        
        self.radio2 = QRadioButton("Super-Resolution(딥러닝)", self)
        self.radio2.move(10, 120)
        self.radio2.resize(500,20)
        self.radio2.clicked.connect(self.radioButton_clicked)
        
 
        imgopenButton.setGeometry(10, 30, 100, 30)
        convertButton.setGeometry(110, 30, 100, 30)
        exportButton.setGeometry(210, 30, 100, 30)
        quitButton.setGeometry(310, 30, 100, 30)
        realtimeButton.setGeometry(10, 150, 100, 30)
        
        
        imgopenButton.clicked.connect(self.IMGOpenFunction)
        convertButton.clicked.connect(self.convertFucntion)
        exportButton.clicked.connect(self.exportFunction)        
        quitButton.clicked.connect(self.quitFunction)
        realtimeButton.clicked.connect(self.realtimeFunction)
    
    def IMGOpenFunction(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './examples') 
        fname = './examples/' + fname[0].split('/')[-1] # 한글 경로 오류로 수동 지정
        print(fname)
        self.img = cv.imread(fname)
        if self.img is None : sys.exit('파일을 찾을 수 없습니다.')        
        # self.img_show = np.copy(self.img)
        cv.imshow('Original', self.img)
    
    def convertFucntion(self):
        if self.scale == '2':
            model = "models/LapSRN_x2.pb"
        elif self.scale == '4':
            model = "models/LapSRN_x4.pb"
        elif self.scale == '8':
            model = "models/LapSRN_x8.pb"
        
        modelName = "lapsrn" # model.split(os.path.sep)[-1].split("_")[0].lower()
        modelScale = int(self.scale)
         
        sr = cv.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(model)
        sr.setModel(modelName, modelScale)
        
        if self.method == "bicubic":
            print("bicubic")
            start = time.time()
            self.bicubic = cv.resize(self.img, (self.img.shape[1]*modelScale, self.img.shape[0]*modelScale))
            end = time.time()
            cv.imshow("Bicubic", self.bicubic)
        elif self.method == "super":
            print("super-resolution")
            start = time.time()
            self.upscaled = sr.upsample(self.img)
            end = time.time()            
            cv.imshow("Super Resolution", self.upscaled)
    
    def exportFunction(self):
        cv.imwrite("result/result.png", self.upscaled)
        
    def quitFunction(self):
        cv.destroyAllWindows()
        self.close()
        
    def realtimeFunction(self):
        model = "models/FSRCNN_x3.pb"
        modelName = "fsrcnn"
        modelScale = 3
        
        sr = cv.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(model)
        sr.setModel(modelName, modelScale)
        print("[INFO] starting video stream...")

        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened(): self.close
        while True:
            ret, frame = self.cap.read()
            if not ret: break
            frame = cv.resize(frame, (200, 150))
            upscaled = sr.upsample(frame)            
            bicubic = cv.resize(frame, (upscaled.shape[1], upscaled.shape[0]), interpolation=cv.INTER_CUBIC)

            cv.imshow('original', frame)
            cv.imshow('super-resolution', upscaled)
            cv.imshow('bicubic', bicubic)
            
            if cv.waitKey(1) == ord('q'):
                break
            
        cv.destroyAllWindows()
        self.close()
        
    def scalepick(self, text):
        self.scale = text
       
    def radioButton_clicked(self):
        if self.radio1.isChecked():
            self.method = "bicubic"
        else:
            self.method = "super"
            
app = QApplication(sys.argv)
win = Resolution()
win.show()
app.exec_()