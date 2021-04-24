from keras import models, layers

from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from contextlib import redirect_stdout

import numpy as np

import tensorflow as tf

import math

import verify_enc

from sklearn.utils import shuffle

import tensorflow as tf
from keras import backend as K



d={}
d=verify_enc.initializare(d)
X_train_list=[]
Y_train_list=[]


X2_train_list=[]
Y2_train_list=[]


X3_train_list=[]
Y3_train_list=[]




'''
print ("Am ajuns la date")

false = verify_enc.read_file('false.csv')
true = verify_enc.read_file('true.csv')
false2 = verify_enc.read_file('false2.csv')
for i in true:
    encoding = verify_enc.verify_encoding(i[0],d)
    litere_mari = verify_enc.count_litere_mari(i[0])
    litere_mici = verify_enc.count_litere_mici(i[0])
    litere_peste_f = verify_enc.count_litere_mai_mari_de_f(i[0])
    lungime = verify_enc.get_len(i[0])
    array = []
    array2=[]
    if (encoding == None):
        encoding = 0
    array.append(float(encoding))
    array.append(float(litere_mari))
    array.append(float(litere_mici))
    array.append(float(litere_peste_f))
    array.append(float(lungime))
    X_train_list.append(array)
    Y_train_list.append(int(i[1]))
   
    array2.append(float(encoding))
    X2_train_list.append(array2)
    Y2_train_list.append(int(i[1]))
    
    
for i in false:
    encoding = verify_enc.verify_encoding(i[0],d)
    litere_mari = verify_enc.count_litere_mari(i[0])
    litere_mici = verify_enc.count_litere_mici(i[0])
    litere_peste_f = verify_enc.count_litere_mai_mari_de_f(i[0])
    lungime = verify_enc.get_len(i[0])
    array = []
    if (encoding == None):
        encoding = 0
    array.append(float(encoding))
    array.append(float(litere_mari))
    array.append(float(litere_mici))
    array.append(float(litere_peste_f))
    array.append(float(lungime))
    X_train_list.append(array)
    Y_train_list.append(int(i[1]))
    
print ("Am terminat cu incarcarea primului set de date")
    


print ("Am terminat cu incarcarea setului 2 de date")


for i in false2:
    encoding = verify_enc.verify_encoding(i[0],d)
    array2=[]
    if (encoding == None):
        encoding = 0
    array2.append(float(encoding))
    X2_train_list.append(array2)
    Y2_train_list.append(int(i[1]))
    
    
print ("Am terminat cu incarcarea setului 3 de date")




def train_1():
    X_train=np.array(X_train_list)
    Y_train=np.array(Y_train_list)
    
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    
    model = models.Sequential()
    model.add(layers.Dense(5, activation='relu', input_shape=[X_train.shape[1]]))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Conv1D(filters=256, kernel_size=5, padding='same', activation='relu'))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(16, activation='relu'))
    
    model.add(layers.Dense(units=1, activation="sigmoid"))
    X_train_scaled, Y_train=shuffle(X_train_scaled, Y_train)
    model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train_scaled, Y_train, validation_split=0.2, epochs=10)
    model.save("model2.h5")



print ("Am terminat cu primul model")


def train_2():
    X2_train=np.array(X2_train_list)
    Y2_train=np.array(Y2_train_list)
    
    scaler2 = StandardScaler()
    scaler2.fit(X2_train)
    X2_train_scaled = scaler2.transform(X2_train)
    
    model2 = models.Sequential()
    model2.add(layers.Dense(4, activation='relu', input_shape=[X2_train.shape[1]]))
    model2.add(layers.Dense(8, activation='relu'))
    model2.add(layers.Dense(16, activation='relu'))
    model2.add(layers.Dense(8, activation='relu'))
    
    model2.add(layers.Dense(units=1, activation="sigmoid"))
    X2_train_scaled, Y2_train=shuffle(X2_train_scaled, Y2_train)
    model2.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])
    model2.fit(X2_train_scaled, Y2_train, validation_split=0.1, epochs=5)
    model2.save("model3.h5")
    print ("Am terminat cu al doilea model")
'''




true_ads = verify_enc.read_file('true_extins.csv')
false_ads = verify_enc.read_file('false_extins.csv')

d={}
d=verify_enc.initializare_extins()
for i in true_ads:
    encoding = verify_enc.verify_encoding(i[0],d)
    litere_mari = verify_enc.count_litere_mari(i[0])
    litere_mici = verify_enc.count_litere_mici(i[0])
    litere_peste_f = verify_enc.count_litere_mai_mari_de_f(i[0])
    lungime = verify_enc.get_len(i[0])
    cifre = verify_enc.count_cifre(i[0])
    puncte = verify_enc.count_dots(i[0])
    minus = verify_enc.count_lines(i[0])
    underscore = verify_enc.count_underscore(i[0])
    slash = verify_enc.count_slashes(i[0])
    entropy = verify_enc.get_entropy(i[0])
    all_lens = verify_enc.get_every_len(i[0])
    array = []
    if (encoding == None):
        encoding = 0
    array.append(float(encoding))
    array.append(float(litere_mari))
    array.append(float(litere_mici))
    array.append(float(litere_peste_f))
    array.append(float(lungime))
    array.append(float(cifre))
    array.append(float(puncte))
    array.append(float(minus))
    array.append(float(underscore))
    array.append(float(slash))
    array.append(float(entropy))
    for z in all_lens:
        array.append(float(z))
    X3_train_list.append(array)
    Y3_train_list.append(int(i[1]))
    
for i in false_ads:
    encoding = verify_enc.verify_encoding(i[0],d)
    litere_mari = verify_enc.count_litere_mari(i[0])
    litere_mici = verify_enc.count_litere_mici(i[0])
    litere_peste_f = verify_enc.count_litere_mai_mari_de_f(i[0])
    lungime = verify_enc.get_len(i[0])
    cifre = verify_enc.count_cifre(i[0])
    puncte = verify_enc.count_dots(i[0])
    minus = verify_enc.count_lines(i[0])
    underscore = verify_enc.count_underscore(i[0])
    slash = verify_enc.count_slashes(i[0])
    entropy = verify_enc.get_entropy(i[0])
    all_lens = verify_enc.get_every_len(i[0])
    array = []
    if (encoding == None):
        encoding = 0
    array.append(float(encoding))
    array.append(float(litere_mari))
    array.append(float(litere_mici))
    array.append(float(litere_peste_f))
    array.append(float(lungime))
    array.append(float(cifre))
    array.append(float(puncte))
    array.append(float(minus))
    array.append(float(underscore))
    array.append(float(slash))
    array.append(float(entropy))
    for z in all_lens:
        array.append(float(z))
    X3_train_list.append(array)
    Y3_train_list.append(int(i[1]))
    



def train_3():
    X3_train=np.array(X3_train_list)
    Y3_train=np.array(Y3_train_list)
    
    scaler = StandardScaler()
    scaler.fit(X3_train)
    X3_train_scaled = scaler.transform(X3_train)
    print ("AICI E",X3_train.shape[1])
    model = models.Sequential()
    model.add(layers.Dense(4, activation='relu', input_shape=[X3_train.shape[1]]))
    model.add(layers.Dense(8, activation='relu'))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(8, activation='relu'))
    
    model.add(layers.Dense(units=1, activation="sigmoid"))
    X3_train_scaled, Y3_train=shuffle(X3_train_scaled, Y3_train)
    model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X3_train_scaled, Y3_train, validation_split=0.2, epochs=20)
    model.save("model4.h5")
#train_1()
#train_2()
train_3()
'''
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())
'''