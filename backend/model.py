import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

MODEL_PATH = "backend/model.pkl"

class TimeSeriesModel:
    def __init__(self):
        self.model = None

    def fit(self, X, y):
        self.model = LinearRegression()
        self.model.fit(X, y)
        self.save()

    def predict(self, X):
        if self.model is None:
            self.load()
        if self.model is not None:
            return self.model.predict(X)
        return np.zeros(len(X))

    def save(self):
        if self.model is not None:
            joblib.dump(self.model, MODEL_PATH)

    def load(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
        else:
            self.model = None

# Singleton instance
ts_model = TimeSeriesModel()