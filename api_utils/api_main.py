from fastapi import FastAPI, HTTPException, Depends, status
import pickle
import os
import pandas as pd
from pydantic import BaseModel
import streamlit as st

path = os.path.dirname(__file__)
# Model Path
MODEL_PATH = path+"/model/rf_model_to_predict_heartDisease"
app = FastAPI()

@app.post("/get_predictions")
def get_predictions():
    df =pd.read_csv("streamlit/data/df.csv")
    log_model = pickle.load(open(MODEL_PATH, "rb"))
    prediction = log_model.predict(df)
    prediction_prob = log_model.predict_proba(df)
    pred = (100*prediction_prob[0][1]).round(0)
    return {"prediction":prediction,"percentage": pred}

