# import os 
# import time 
# import socket
# import sys

# def server():
# 	IP_PORT =  ('0.0.0.0',9999)
# 	sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	sk.bind(IP_PORT)
# 	sk.listen(5)
# 	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 	conn,addr = sk.accept()
# 	data = conn.recv(1024)
# 	file_name = 'record.wav'
# 	path = os.path.join(BASE_DIR,file_name)
# 	with open(path,'wb') as fp:
# 		while True:
# 			data = conn.recv(1024)
# 			if data:
# 				fp.write(data)
# 			else:
# 				break


# def client():
# 	IP_PORT = ('10.42.0.69',9999)
# 	sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	sk.connect(IP_PORT)
# 	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 	path = 'record.wav'
# 	path = os.path.join(BASE_DIR,path)
# 	with open(path,'rb') as fp:
# 		data = fp.read()
# 		sk.sendall(data)

# mode = sys.argv[1]
# if mode == 'server':
# 	server()
# elif mode=='client':
# 	client()


# -*- coding:utf-8 -*-
import requests
import json
import sys

# url = 'http://10.42.0.69:8000/upload_file/'
# path = 'record.wav'
# with open(path, 'rb') as fp:
#     data = fp.read()

# post = {
#     'file':data,
#     };

# resp = requests.post(url, files=post) #post提交数据

# print(resp.text)

def upload_record_name():
    url = 'http://10.42.0.69:8000/upload_record_name/'
    path = 'record.wav'
    with open(path, 'rb') as fp:
        data = fp.read()
    post = {
        'file':data,
        };
    resp = requests.post(url, files=post) #post提交数据
    print(resp.text)

def upload_record_id():
    url = 'http://10.42.0.69:8000/upload_record_id/'
    path = 'record.wav'
    with open(path, 'rb') as fp:
        data = fp.read()
    post = {
        'file':data,
        };
    resp = requests.post(url, files=post) #post提交数据
    return resp.text

def predict_voice():   
    url = 'http://10.42.0.69:8000/predict_voice/'
    path = 'record.wav'
    with open(path, 'rb') as fp:
        data = fp.read()
    post = {
        'file':data,
        };
    resp = requests.post(url, files=post) #post提交数据
    return resp.text

def train(predicted_id):
    url = 'http://10.42.0.69:8000/train/'
    data = {
        'predicted_id':predicted_id,
        };
    resp = requests.post(url, data) #post提交数据

print(predict_voice())