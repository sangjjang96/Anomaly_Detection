# -*- coding: utf-8 -*-
"""protect.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12GF1RHFTCyeXuGZwz4bQIBSURPVRmKAi

# **랜덤 포레스트를 이용한 방화벽 로그분석 프로젝트**
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error

df = pd.read_csv("/content/drive/MyDrive/protect/04_hashed.csv")

df1 = df[df['Action'] != 0]

le = preprocessing.LabelEncoder()
for i in range(9):
  df1.iloc[:,i] = le.fit_transform(df1.iloc[:,i])

target_data = df1['Action']
train_data = df1.drop('Action', axis=1)

x_train, x_test, y_train, y_test = train_test_split(train_data,target_data, shuffle = False, random_state = None)


forest = RandomForestClassifier(n_estimators=10)
forest.fit(x_train, y_train)

from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score 
def print_score(classifier,x_train,y_train,x_test,y_test,train=True):
  if train ==True:
    print("Training results:\n")
    print('Accuracy Score: {0:4f}\n'.format(accuracy_score(y_train,classifier.predict(x_train))))
    print('Classification Report:\n{}\n'.format(classification_report(y_train,classifier.predict(x_train))))
    print('Confusion Matrix:\n{}\n'.format(confusion_matrix(y_train,classifier.predict(x_train))))
    res = cross_val_score(classifier,x_train,y_train,cv=10,n_jobs=-1,scoring='accuracy')
    print('Average Accuracy:\t{0:.4f}\n'.format(res.mean()))
    print('Standard Deviation:\t{0:.4f}'.format(res.std()))
  elif train == False:
    print("Test results:\n")
    print('Accuracy Score:{0:.4f}\n'.format(accuracy_score(y_test,classifier.predict(x_test))))
    print('Classification Report:\n{}\n'.format(classification_report(y_test,classifier.predict(x_test))))
    print('Confusion Matrix:\n{}\n'.format(confusion_matrix(y_test,classifier.predict(x_test))))


print_score(forest, x_train,y_train,x_test,y_test,train=True)
print_score(forest,x_train,y_train,x_test,y_test,train=False)

predict = forest.predict(x_test)

x_test["predict"] = predict

x_test["Action"] = y_test

print(x_test.head(30))

x_test.to_csv("result.csv",index=False)