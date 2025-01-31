# -*- coding: utf-8 -*-
"""fertilizer_recommendation_system.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16GLUKuhYH-Ly-umKdRISMGWfmRIQeq8y
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings
import imblearn
from imblearn.over_sampling import SMOTE
from collections import Counter

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

from sklearn.neighbors import  KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPRegressor
import xgboost
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, confusion_matrix

import pickle

import warnings
warnings.filterwarnings("ignore")

# %matplotlib inline

"""Reading the data"""

data = pd.read_csv('/content/Fertilizer Prediction.csv')

data.head()

data.info()

"""Data Preprocessing"""

data.rename(columns={'Humidity ':'Humidity','Soil Type':'Soil_Type','Crop Type':'Crop_Type','Fertilizer Name':'Fertilizer'},inplace=True)

data.nunique()

data.isna().sum()

data.describe(include='all')

"""Visualization"""

labels = data["Fertilizer"].unique()
counts = list(data["Fertilizer"].value_counts())

plt.figure(figsize = (9,5))
plt.barh(labels, counts)

for index, value in enumerate(counts):
    plt.text(value, index,
             str(value))
plt.show()

#Defining function for Continuous and catogorical variable
def plot_conti(x):
    fig, axes = plt.subplots(nrows=1,ncols=3,figsize=(15,5),tight_layout=True)
    axes[0].set_title('Histogram')
    sns.histplot(x,ax=axes[0])
    axes[1].set_title('Checking Outliers')
    sns.boxplot(x,ax=axes[1])
    axes[2].set_title('Relation with output variable')
    sns.boxplot(y = x,x = data.Fertilizer)

def plot_cato(x):
    fig, axes = plt.subplots(nrows=1,ncols=2,figsize=(15,5),tight_layout=True)
    axes[0].set_title('Count Plot')
    sns.countplot(x,ax=axes[0])
    axes[1].set_title('Relation with output variable')
    sns.countplot(x = x,hue = data.Fertilizer, ax=axes[1])

plot_conti(data.Temparature)

plot_conti(data.Humidity)

plot_conti(data.Moisture)

plot_cato(data.Soil_Type)

plot_cato(data.Crop_Type)

plot_conti(data.Nitrogen)

plot_conti(data.Potassium)

plot_conti(data.Phosphorous)

"""Label Encoding"""

#encoding the labels for categorical variables
from sklearn.preprocessing import LabelEncoder
#encoding Soil Type variable
encode_soil = LabelEncoder()

#fitting the label encoder
data.Soil_Type = encode_soil.fit_transform(data.Soil_Type)

#creating the DataFrame
Soil_Type = pd.DataFrame(zip(encode_soil.classes_,encode_soil.transform(encode_soil.classes_)),columns=['Original','Encoded'])
Soil_Type = Soil_Type.set_index('Original')
Soil_Type

#encoding Crop Type variable
encode_crop = LabelEncoder()

#fitting the label encoder
data.Crop_Type = encode_crop.fit_transform(data.Crop_Type)

#creating the DataFrame
Crop_Type = pd.DataFrame(zip(encode_crop.classes_,encode_crop.transform(encode_crop.classes_)),columns=['Original','Encoded'])
Crop_Type = Crop_Type.set_index('Original')
Crop_Type

#encoding Fertilizer variable
encode_ferti = LabelEncoder()

#fitting the label encoder
data.Fertilizer = encode_ferti.fit_transform(data.Fertilizer)

#creating the DataFrame
Fertilizer = pd.DataFrame(zip(encode_ferti.classes_,encode_ferti.transform(encode_ferti.classes_)),columns=['Original','Encoded'])
Fertilizer = Fertilizer.set_index('Original')
Fertilizer

#splitting the dataset
x = data[data.columns[:-1]]
y = data[data.columns[-1]]

#train and test split
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2,random_state=1)

x_train.info()

"""Model Building"""

#Logistic Regression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score  #mean_absolute_percentage_error

from sklearn.ensemble import RandomForestClassifier
rand = RandomForestClassifier()

pred_rand = rand.fit(x_train,y_train).predict(x_test)

print(classification_report(y_test,pred_rand))

y_pred=rand.predict(x_test)

lr_MSE=mean_squared_error(y_test,y_pred)
lr_RMSE=np.sqrt(pred_rand)
lr_MAE=mean_absolute_error(y_test,y_pred)
lr_r2score=r2_score(y_test,y_pred)

print("Mean Square Error :",lr_MSE)
print("\nRoot Mean Square Error :",lr_RMSE)
print("\nMean Absolute Error :",lr_MAE)
print("\nAccuracy :",lr_r2score*100,"%")

#### KNN Classification
error_rate = []
for i in range(1, 50):
    pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors = i))
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy at k = {i} is {accuracy}")
    error_rate.append(np.mean(predictions != y_test))

plt.figure(figsize=(10,6))
plt.plot(range(1,50),error_rate,color='blue', linestyle='dashed',
         marker='o',markerfacecolor='red', markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')
print("Minimum error:-",min(error_rate),"at K =",error_rate.index(min(error_rate))+1)

###### SVM Classification model
svm_pipeline = make_pipeline(StandardScaler(), SVC(probability=True))
svm_pipeline.fit(x_train, y_train)

predictions = svm_pipeline.predict(x_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy on Test Data: {accuracy*100}%")
plt.figure(figsize = (15,9))
sns.heatmap(confusion_matrix(y_test, predictions), annot = True)
plt.title("Confusion Matrix for Test Data")
plt.show()

print()

predictions = svm_pipeline.predict(x.values)
accuracy = accuracy_score(y, predictions)
print(f"Accuracy on Whole Data: {accuracy*100}%")
plt.figure(figsize = (15,9))
sns.heatmap(confusion_matrix(y, predictions), annot = True)
plt.title("Confusion Matrix for Whole Data")
plt.show()

##### Random Forest Classifier
rf_pipeline = make_pipeline(StandardScaler(), RandomForestClassifier(random_state = 18))
rf_pipeline.fit(x_train, y_train)

predictions = rf_pipeline.predict(x_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy on Test Data: {accuracy*100}%")
plt.figure(figsize = (9,9))
sns.heatmap(confusion_matrix(y_test, predictions), annot = True)
plt.title("Confusion Matrix for Test Data")
plt.show()

print()

predictions = rf_pipeline.predict(x.values)
accuracy = accuracy_score(y, predictions)
print(f"Accuracy on Whole Data: {accuracy*100}%")
plt.figure(figsize = (9,9))
sns.heatmap(confusion_matrix(y, predictions), annot = True)
plt.title("Confusion Matrix for Whole Data")
plt.show()

##### XGB classifier
xgb_pipeline = make_pipeline(StandardScaler(), XGBClassifier(random_state = 18))
xgb_pipeline.fit(x_train, y_train)

# Accuray On Test Data
predictions = xgb_pipeline.predict(x_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy on Test Data: {accuracy*100}%")
plt.figure(figsize = (15,9))
sns.heatmap(confusion_matrix(y_test, predictions), annot = True)
plt.title("Confusion Matrix for Test Data")
plt.show()

print()

# Accuray On Whole Data
predictions = xgb_pipeline.predict(x.values)
accuracy = accuracy_score(y, predictions)
print(f"Accuracy on Whole Data: {accuracy*100}%")
plt.figure(figsize = (15,9))
sns.heatmap(confusion_matrix(y, predictions), annot = True)
plt.title("Confusion Matrix for Whole Data")
plt.show()

model = Pipeline([
    ('scaler', StandardScaler()),
    ('mlp', MLPRegressor(hidden_layer_sizes=(64,32), activation='relu', solver='adam', max_iter=1000))
])

model.fit(x_train, y_train)

# Evaluate the performance of the model on the training data
train_score = model.score(x_train, y_train)
print('Training score:', train_score)

# Evaluate the performance of the model on the testing data
test_score = model.score(x_test, y_test)
print('Testing score:', test_score)

y_pred = pipeline.predict(x_test)

scaler = StandardScaler()
X_train = scaler.fit_transform(x_train)
X_test = scaler.transform(x_test)

model = MLPRegressor(hidden_layer_sizes=(64,32), activation='relu', solver='adam', max_iter=1000, random_state=42)
model.fit(X_train, y_train)

train_score = model.score(X_train, y_train)
print('Training score:', train_score)

test_score = model.score(X_test, y_test)
print('Testing score:', test_score)

##### Back Propagation
encoder = LabelEncoder()
y = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

input_layer_size = X_train.shape[1]
hidden_layer_size = 32
output_layer_size = len(np.unique(y_train))

# Initialize the weights randomly
W1 = np.random.randn(input_layer_size, hidden_layer_size) / np.sqrt(input_layer_size)
b1 = np.zeros((1, hidden_layer_size))
W2 = np.random.randn(hidden_layer_size, output_layer_size) / np.sqrt(hidden_layer_size)
b2 = np.zeros((1, output_layer_size))

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    x[x <= 0] = 0
    x[x > 0] = 1
    return x

def softmax(x):
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)

def softmax_derivative(x):
    return softmax(x) * (1 - softmax(x))

def cross_entropy(y_pred, y_true):
    m = y_true.shape[0]
    p = softmax(y_pred)
    log_likelihood = -np.log(p[range(m), y_true])
    loss = np.sum(log_likelihood) / m
    return loss

def cross_entropy_derivative(y_pred, y_true):
    m = y_true.shape[0]
    grad = softmax(y_pred)
    grad[range(m), y_true] -= 1
    grad /= m
    return grad

learning_rate = 0.01
epochs = 1500
train_losses = []
test_losses = []

for i in range(epochs):
    # Forward propagation
    z1 = np.dot(X_train, W1) + b1
    a1 = relu(z1)
    z2 = np.dot(a1, W2) + b2
    y_pred = np.argmax(z2, axis=1)

    # Compute the loss and accuracy on the training set
    train_loss = cross_entropy(z2, y_train)
    train_losses.append(train_loss)
    train_acc = accuracy_score(y_train, y_pred)

    # Backward propagation
    delta2 = cross_entropy_derivative(z2, y_train)
    dW2 = np.dot(a1.T, delta2)
    db2 = np.sum(delta2, axis=0, keepdims=True)
    delta1 = np.dot(delta2, W2.T) * relu_derivative(z1)
    dW1 = np.dot(X_train.T, delta1)
    db1 = np.sum(delta1, axis=0)

    # Update the weights and biases
    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2
    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1

    # Evaluate the model on the test set
    z1_test = np.dot(X_test, W1) + b1
    a1_test = relu(z1_test)
    z2_test = np.dot(a1_test, W2) + b2
    y_pred_test = np.argmax(z2_test, axis=1)
    test_loss = cross_entropy(z2_test, y_test)
    test_losses.append(test_loss)
    test_acc = accuracy_score(y_test, y_pred_test)

    # Print the training loss, training accuracy, test loss, and test accuracy every 100 epochs
    if i % 100 == 0:
        print("Epoch: %d, Train Loss: %f, Train Accuracy: %f, Test Loss: %f, Test Accuracy: %f" % (i, train_loss, train_acc, test_loss, test_acc))

