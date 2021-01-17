# Scores, metrics, diagnosis tools for model evaluations
# Author : Íngrid Munné-Collado
# Date: 04/06/2020

# libraries import
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
import scores_metrics_diagnosis_tools as scores

# y_true= np.array([10,12,14,8,9,5,8,10,12,11,10,15])
# y_pred = np.array([12,14,15,10,7,4,5,8,12,14,13,8])

def forecast_error(ytrue, ypred):
    return ytrue - ypred

def MAPE(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def RMSE(y_true, y_pred):
    return sqrt(mean_squared_error(y_true, y_pred))

def bias(y_true, y_pred):
    return np.mean(y_true - y_pred)

# error = forecast_error(y_true, y_pred)
# MAPE= MAPE(y_true, y_pred)
# RMSE= RMSE(y_true, y_pred)
# bias= bias(y_true, y_pred)
# mae = mean_absolute_error(y_true, y_pred)
