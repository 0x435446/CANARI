# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 00:15:25 2021

@author: mihai
"""

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
from tensorflow.keras.models import load_model
tf.get_logger().setLevel('INFO')

def check_model_1(word):
    model=load_model("./modules/MachineLearning/models/model2.h5")
    crs=[]
    d={}
    d=verify_enc.initializare(d)
    test = []
    encoding = verify_enc.verify_encoding(word,d)
    litere_mari = verify_enc.count_litere_mari(word)
    litere_mici = verify_enc.count_litere_mici(word)
    litere_peste_f = verify_enc.count_litere_mai_mari_de_f(word)
    count_cifre = verify_enc.count_cifre(word)
    lungime = verify_enc.get_len(word)
    test.append(float(encoding))
    test.append(float(litere_mari))
    test.append(float(litere_mici))
    test.append(float(litere_peste_f))
    test.append(float(lungime))
    #test.append(float(count_cifre))
    crs.append(test)
    X_train=np.array(crs)
    # =============================================================================
    # scaler = StandardScaler()
    # test_scaled=scaler.fit(X_train)
    # =============================================================================
    out = model.predict(crs)
    print (int(out[0][0]))
    
    
def check_model_2(word):
    model=load_model("./modules/MachineLearning/models/model3.h5")
    crs=[]
    d={}
    d=verify_enc.initializare(d)
    test = []
    encoding = verify_enc.verify_encoding(word,d)
    test.append(float(encoding))
    #test.append(float(count_cifre))
    crs.append(test)
    X_train=np.array(crs)
    # =============================================================================
    # scaler = StandardScaler()
    # test_scaled=scaler.fit(X_train)
    # =============================================================================
    out = model.predict(crs)
    print (int(out[0][0]))
    print (encoding)

def check_model_3(word):
    model=load_model("./modules/MachineLearning/models/model4.5.h5")
    crs=[]
    d={}
    d=verify_enc.initializare_extins()
    test = []
    encoding = verify_enc.verify_encoding(word,d)
    litere_mari = verify_enc.count_litere_mari(word)
    litere_mici = verify_enc.count_litere_mici(word)
    litere_peste_f = verify_enc.count_litere_mai_mari_de_f(word)
    lungime = verify_enc.get_len(word)
    cifre = verify_enc.count_cifre(word)
    puncte = verify_enc.count_dots(word)
    minus = verify_enc.count_lines(word)
    underscore = verify_enc.count_underscore(word)
    slash = verify_enc.count_slashes(word)
    entropy = verify_enc.get_entropy(word)
    all_lens = verify_enc.get_every_len(word)
    test.append(float(encoding))
    test.append(float(litere_mari))
    test.append(float(litere_mici))
    test.append(float(litere_peste_f))
    test.append(float(lungime))
    test.append(float(cifre))
    test.append(float(puncte))
    test.append(float(minus))
    test.append(float(underscore))
    test.append(float(slash))
    test.append(float(entropy))
    for z in all_lens:
        test.append(float(z))
    crs.append(test)
    X_train=np.array(crs)
    # =============================================================================
    # scaler = StandardScaler()
    # test_scaled=scaler.fit(X_train)
    # =============================================================================
    out = model.predict(crs)
    return int(out[0][0])



def check_model_4(word,d):
    model=load_model("./modules/MachineLearning/models/model4.5.h5")
    crs=[]
    test = []
    encoding = verify_enc.verify_encoding(word,d)
    if (encoding == None):
        encoding = 0
    litere_mari = verify_enc.count_litere_mari(word)
    litere_mici = verify_enc.count_litere_mici(word)
    litere_peste_f = verify_enc.count_litere_mai_mari_de_f(word)
    lungime = verify_enc.get_len(word)
    cifre = verify_enc.count_cifre(word)
    puncte = verify_enc.count_dots(word)
    minus = verify_enc.count_lines(word)
    underscore = verify_enc.count_underscore(word)
    slash = verify_enc.count_slashes(word)
    entropy = verify_enc.get_entropy(word)
    all_lens = verify_enc.get_every_len(word)
    test.append(float(encoding))
    test.append(float(litere_mari))
    test.append(float(litere_mici))
    test.append(float(litere_peste_f))
    test.append(float(lungime))
    test.append(float(cifre))
    test.append(float(puncte))
    test.append(float(minus))
    test.append(float(underscore))
    test.append(float(slash))
    test.append(float(entropy))
    for z in all_lens:
        test.append(float(z))
    crs.append(test)
    X_train=np.array(crs)
    # =============================================================================
    # scaler = StandardScaler()
    # test_scaled=scaler.fit(X_train)
    # =============================================================================
    out = model.predict(crs)
    return int(out[0][0])