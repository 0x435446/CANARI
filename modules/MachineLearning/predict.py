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
    return (int(out[0][0]))
    
    
def check_model_2(word):
    model=load_model("./modules/MachineLearning/models/model3.h5")
    crs=[]
    d={}
    d=verify_enc.initializare(d)
    test = []
    encoding = verify_enc.verify_encoding(word,d)
    print (encoding)
    test.append(float(encoding))
    #test.append(float(count_cifre))
    crs.append(test)
    X_train=np.array(crs)
    # =============================================================================
    # scaler = StandardScaler()
    # test_scaled=scaler.fit(X_train)
    # =============================================================================
    out = model.predict(crs)
    return (int(out[0][0]))

def check_model_3(word):
    model=load_model("./modules/MachineLearning/models/model4.h5")
    crs=[]
    d={}
    d=verify_enc.initializare(d)
    test = []
    encoding = verify_enc.verify_encoding(word,d)
    litere_mari = verify_enc.count_litere_mari(word)
    litere_mici = verify_enc.count_litere_mici(word)
    litere_peste_f = verify_enc.count_litere_mai_mari_de_f(word)
    lungime = verify_enc.get_len(word)
    cifre = verify_enc.count_cifre(word)
    puncte = verify_enc.count_dots(word)
    minus = verify_enc.count_lines(word)
    all_lens = verify_enc.get_every_len(word)
    test.append(float(encoding))
    test.append(float(litere_mari))
    test.append(float(litere_mici))
    test.append(float(litere_peste_f))
    test.append(float(lungime))
    test.append(float(cifre))
    test.append(float(puncte))
    test.append(float(minus))
    for z in all_lens:
        test.append(float(z))
    crs.append(test)
    X_train=np.array(crs)
    # =============================================================================
    # scaler = StandardScaler()
    # test_scaled=scaler.fit(X_train)
    # =============================================================================
    out = model.predict(crs)
    return (int(out[0][0]))

    


#check_model_1(word)
#check_model_2(word)
#check_model_3(word)