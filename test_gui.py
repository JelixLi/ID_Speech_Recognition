import tkinter as tk
from PIL import Image,ImageTk
import time
import os
from multiprocessing import Process
import shutil

from models.conv import GatedConv
import pre_transform_2 as pt2
import enhance_speach as es

from name_dict import name_dict

import os
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time

def predict_voice(path):   
    modelpath = "new_speaker_model/"   
    gmm_files = [os.path.join(modelpath,fname) for fname in 
                  os.listdir(modelpath) if fname.endswith('.gmm')]
    models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
                  in gmm_files]  
    print(path)
    sr,audio = read(path)
    vector   = extract_features(audio,sr)
    
    log_likelihood = np.zeros(len(models)) 
    
    for i in range(len(models)):
        gmm    = models[i]         #checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
    
    winner = np.argmax(log_likelihood)
    print("\tdetected as - ", speakers[winner])
    return speakers[winner]


model = GatedConv.load("pretrained/gated-conv.pth")

def predict():
    input_file_src = "record.wav"
    output_file_src = "record_out.wav"
    es.denoise(input_file_src,output_file_src)
    text = model.predict(output_file_src)
    text = pt2.predict2(text)
    return text

window = tk.Tk()
window.title('my window')
window.geometry('250x300')
window['background'] = 'white'

def jump_to_register():
    base_window.destroy()
    register_window.init_frame()

def jump_to_check():
    base_window.destroy()
    check_window.init_frame()

def jump_to_main_from_check():
    check_window.destroy()
    base_window.init_frame()


class Recorder():
    def __init__(self,window):
        self.window = window
        self.rec_proc = Process(target=self.run_record_proc) 

    def init_frame(self):
        self.canvas = tk.Canvas(self.window, width=465, height=22, bg="white")
        self.canvas.pack()

    def run_record_proc(self):
        os.system('sh play.sh')

    def record(self):
        rec_proc = Process(target=self.run_record_proc) 
        self.clear()
        rec_proc.start()
        time.sleep(0.3)
        self.progress()
        rec_proc.join()

    def progress(self):
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="RoyalBlue")
        x = 200  # 未知变量，可更改
        n = 465 / x  # 465是矩形填充满的次数
        for i in range(x):
            n = n + 465 / x
            self.canvas.coords(fill_line, (0, 0, n, 60))
            self.window.update()
            time.sleep(0.02)  # 控制进度条流动的速度

    def clear(self):     
        # 清空进度条
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
        x = 200  # 未知变量，可更改
        n = 465 / x  # 465是矩形填充满的次数
        for t in range(x):
            n = n + 465 / x
            # 以矩形的长度作为变量值更新
            self.canvas.coords(fill_line, (0, 0, n, 60))
            self.window.update()
            time.sleep(0)  # 时间为0，即飞速清空进度条


class BufferWindow():
    def __init__(self,window):
        self.base_window = window

    def init_frame(self):
        self.window = tk.Frame(self.base_window)
        self.window['background'] = 'white'
        self.window.pack()
        self.image = Image.open("neu_2.jpeg")  
        self.photo = ImageTk.PhotoImage(self.image)  
        self.theLabel = tk.Label(self.window,image=self.photo)
        self.theLabel.pack()

        l = tk.Label(self.window, 
            bg='white',height=5)
        l.pack() 

        self.var = tk.StringVar()    # 这时文字变量储存器
        l = tk.Label(self.window, 
            textvariable=self.var,   # 使用 textvariable 替换 text, 因为这个可以变化
            bg='white', font=('Helvetica', 15), width=50, height=4)
        l.pack() 

        self.var.set('Processing Data ... Please Wait .')

    def destroy(self):
        self.window.destroy()

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path,i)
        os.remove(c_path)


class RegisterWindow():
    def __init__(self,window):
        self.base_window = window
        self.predicted_id = None
        self.buffer_window = BufferWindow(window)

    def init_frame(self):
        self.window = tk.Frame(self.base_window)
        self.window['background'] = 'white'
        self.window.pack()
        self.image = Image.open("neu_2.jpeg")  
        self.photo = ImageTk.PhotoImage(self.image)  
        self.theLabel = tk.Label(self.window,image=self.photo)
        self.theLabel.pack()

        self.var = tk.StringVar()    # 这时文字变量储存器
        l = tk.Label(self.window, 
            textvariable=self.var,   # 使用 textvariable 替换 text, 因为这个可以变化
            bg='white', font=('Helvetica', 12), width=50, height=4)
        l.pack() 

        self.var.set('Please Record Your ID')

        b = tk.Button(self.window, 
            text='Record Student ID',      # 显示在按钮上的文字
            font=("Arial", 10),
            width=50, height=3, 
            command=self.record_student_id)     # 点击按钮式执行的命令
        b['background'] = 'Azure'
        b.pack()    # 按钮位置

        b = tk.Button(self.window, 
            text='Record Name',      # 显示在按钮上的文字
            font=("Arial", 10),
            width=50, height=3, 
            command=self.record_name)     # 点击按钮式执行的命令
        b['background'] = 'Azure'
        b.pack()    # 按钮位置

        b = tk.Button(self.window, 
            text='Back',      # 显示在按钮上的文字
            font=("Arial", 10),
            width=50, height=3, 
            command=self.jump_to_main_from_register)     # 点击按钮式执行的命令
        b['background'] = 'Azure'
        b.pack()    # 按钮位置

        l = tk.Label(self.window, 
            bg='white',height=1)
        l.pack() 

        self.recorder = Recorder(self.window)
        self.recorder.init_frame()

    def jump_to_main_from_register(self):
        register_window.destroy()
        self.buffer_window.init_frame()
        train_path = 'train_src/'
        predicted_id = self.predicted_id
        if os.path.isdir(train_path+predicted_id):
            del_file(train_path+predicted_id)
            os.removedirs(train_path+predicted_id)
        os.mkdir(train_path+predicted_id)
        shutil.move('record_id.wav',train_path+predicted_id+'/record_id.wav')
        shutil.move('record_name.wav',train_path+predicted_id+'/record_name.wav')
        with open('train.txt','w') as f:
            f.write(predicted_id+'/record_id.wav')
            f.write('\n')
            f.write(predicted_id+'/record_name.wav')
        os.system('python train_models.py')
        self.buffer_window.destroy()
        base_window.init_frame()

    def destroy(self):
        self.window.destroy()

    def record_student_id(self):    
        self.recorder.record()
        self.predicted_id = predict()
        self.var.set(self.predicted_id)
        if os.path.exists('record_id.wav'):
            os.remove('record_id.wav')
        os.rename('record.wav','record_id.wav')

    def record_name(self):
        self.recorder.record()
        if os.path.exists('record_name.wav'):
            os.remove('record_name.wav')
        os.rename('record.wav','record_name.wav')

class CheckWindow():
    def __init__(self,window):
        self.base_window = window

    def init_frame(self):
        self.window = tk.Frame(self.base_window)
        self.window['background'] = 'white'
        self.window.pack()
        self.image = Image.open("neu_2.jpeg")  
        self.photo = ImageTk.PhotoImage(self.image)  
        self.theLabel = tk.Label(self.window,image=self.photo)
        self.theLabel.pack()

        self.var = tk.StringVar()    # 这时文字变量储存器
        l = tk.Label(self.window, 
            textvariable=self.var,   # 使用 textvariable 替换 text, 因为这个可以变化
            bg='white', font=('Helvetica', 12), width=50, height=4)
        l.pack() 

        self.var.set('Please Record Your Name')

        b = tk.Button(self.window, 
            text='Check',      # 显示在按钮上的文字
            font=("Arial", 10),
            width=50, height=3, 
            command=self.record_name)     # 点击按钮式执行的命令
        b['background'] = 'Azure'
        b.pack()    # 按钮位置

        b = tk.Button(self.window, 
            text='Back',      # 显示在按钮上的文字
            font=("Arial", 10),
            width=50, height=3, 
            command=jump_to_main_from_check)     # 点击按钮式执行的命令
        b['background'] = 'Azure'
        b.pack()    # 按钮位置

        l = tk.Label(self.window, 
            bg='white',height=1)
        l.pack() 

        self.recorder = Recorder(self.window)
        self.recorder.init_frame()

    def destroy(self):
        self.window.destroy()

    def record_name(self):
        self.recorder.record()
        predicted_id = predict_voice('record.wav')
        predicted_name = name_dict[predicted_id]
        self.var.set(predicted_name)


class BaseWindow():
    def __init__(self,window):
        self.base_window = window


    def init_frame(self):
        #增加背景图片
        # photo = tk.PhotoImage(file='test.gif')
        self.window = tk.Frame(self.base_window)
        self.window['background'] = 'white'
        self.window.pack()
        self.image = Image.open("neu_2.jpeg")  
        self.photo = ImageTk.PhotoImage(self.image)  
        self.theLabel = tk.Label(self.window,image=self.photo)
        self.theLabel.pack()

        var = tk.StringVar()    # 这时文字变量储存器
        l = tk.Label(self.window, 
            textvariable=var,   # 使用 textvariable 替换 text, 因为这个可以变化
            bg='white', font=('Arial', 12), width=15, height=1)
        l.pack() 

        b = tk.Button(self.window, 
            text='Check',      # 显示在按钮上的文字
            font=("Arial", 10),
            width=50, height=8, 
            command=jump_to_check)     # 点击按钮式执行的命令
        b['background'] = 'Azure'
        b.pack()    # 按钮位置

        l = tk.Label(self.window, 
            bg='white',height=1)
        l.pack() 

        b = tk.Button(self.window, 
            text='Register',      # 显示在按钮上的文字
            font=('Arial', 10),
            width=50, height=8, 
            command=jump_to_register)     # 点击按钮式执行的命令
        b['background'] = 'Azure'
        b.pack()    # 按钮位置

    def destroy(self):
        self.window.destroy()


base_window = BaseWindow(window)
register_window = RegisterWindow(window)
check_window = CheckWindow(window)

base_window.init_frame()

window.mainloop()