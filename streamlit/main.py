import io
import json

import pandas as pd
import numpy as np
import streamlit as st
import base64
import pickle
import sklearn
import getpass
from PIL import Image
import shap
import pickle
# all other imports
import requests
import os
# from streamlit_elements import Elements
import streamlit_shap as st_shap
import streamlit as st
import shap
import streamlit.components.v1 as components
import streamlit_shap

from utils import get_answers_to_ques

###############################################################################

# The code below is for the layout of the page
if "widen" not in st.session_state:
    layout = "centered"
else:
    layout = "wide" if st.session_state.widen else "centered"
if 'predict' not in st.session_state:
    st.session_state.predict = False
path = os.path.dirname(__file__)


st.set_page_config(
    layout=layout,
    page_title='Heart Disease Prediction App',  # String or None. Strings get appended with "• Streamlit".
    # page_icon= path+"/images/hi.png",  # String, anything supported by st.image, or None.

    page_icon= "💖"
)

###############################################################################
# Lets Prepare some data
data = {'18-24':0, '25-29':1,'30-34':2,'35-39':3,'40-44':4,'45-49':5,'50-54':6,'55-59':7,'60-64':8,'65-69':9,'70-74':10,'75-79':11,'80 or older':12}
age_df = pd.DataFrame({'AgeCategory' : data.keys() , 'AgeValue' : data.values() })

###############################################################################
# Define few functions


# bgimage_link = "https://drive.google.com/file/d/1qpO3e_leNXN30DVMkTRo7-LjyxA2lvzY/view?usp=share_link"
# Image from Local
path = os.path.dirname(__file__)
image_file = path+'/images/red_bg.jpeg'

# Image from link
# add_bg_from_local(bgimage_link)

# Model Path
MODEL_PATH = path+"/model/rf_model_to_predict_heartDisease"

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


def featuresTransformations_to_df(agecat_key, bmi_key, gender, race, smoking, alcohol, health_key, diabetic, asthma, stroke, skincancer, kidneydisease) -> pd.DataFrame:
    age_dict = {'18-24':0, '25-29':1,'30-34':2,'35-39':3,'40-44':4,'45-49':5,'50-54':6,'55-59':7,'60-64':8,'65-69':9,'70-74':10,'75-79':11,'80 or older':12}
    health_dict = {'Poor':0,'Fair':1,'Good':2,'Very good':3,'Excellent':4}
    bmi_dict = {'UnderWeight':0,'NormalWeight':1,'OverWeight':2,'Obesity Class I':3,'Obesity Class II':4, 'Obesity Class III':5}
    dict = {"Yes": 1, "No": 0}

    agecat = age_dict.get(agecat_key)
    health = health_dict.get(health_key)
    bmi = bmi_dict.get(bmi_key)
    diabetic = 1 if diabetic == "Yes" else 0
    gender = 1 if gender == "Male" else 0
    race = 1 if race == "White" else 0

    stroke = 1 if stroke == "Yes" else 0
    skincancer = 1 if skincancer == "Yes" else 0
    kidneydisease = 1 if kidneydisease == "Yes" else 0
    asthma = 1 if asthma == "Yes" else 0
    smoking = 1 if smoking == "Yes" else 0
    alcohol = 1 if alcohol == "Yes" else 0


    df = pd.DataFrame({
        "AgeCategory": [agecat],
        "Stroke": [stroke],
        "Diabetic_Yes": [diabetic],
        "KidneyDisease": [kidneydisease],
        "Smoking": [smoking],
        "SkinCancer": [skincancer],
        "Is_Male": [gender],
        "BMI": [bmi],
        "Asthma": [asthma],
        "Race_White": [race],
        "AlcoholDrinking": [alcohol],
        "GenHealth": [health]
    })

    return df

###############################################################################
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body style='background-color: white'>{plot.html()}</body>"
    components.html(shap_html, height=height)

def predict_heart_disease():
    with open('config.json', 'r') as f:
        config = json.load(f)

    endpoint = config['endpoints']['predict']
    add_bg_from_local(image_file)

    st.title("Heart Disease Prediction App")
    st.markdown("Are you worried about the condition of your heart? "
                 "This app will help you to diagnose it!")

    # st.markdown("This App will help you to Diagnose it!")



    st.subheader("General Information:")
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox(
        "Gender",
        options = ["Male", "Female"],
        help="Choose your Gender!",
        )

    with col2:
        agecat_key = st.selectbox(
            "Age Group",
            options=age_df.AgeCategory.unique().tolist(),
            help="Choose a age group you belong to!",
        )

    with col3:
        race = st.selectbox(
            "Race",
            options= ['White', 'Black', 'Asian', 'American Indian/Alaskan Native', 'Hispanic',  'Other'],
            help="Choose your Race!",
        )

        # ['AgeCategory', 'Stroke', 'Diabetic_Yes', 'KidneyDisease', 'Smoking', 'SkinCancer', 'is_Male', 'BMI', 'Asthma',
         # 'Race_White', 'AlcoholDrinking', 'GenHealth']

    st.subheader("Habits:")
    col4, col5 = st.columns(2)

    with col4:
        smoking = st.selectbox(
            "Do you Smoke?",
            options=["Yes", "No"],
            help="Whether you smoke or Not!",
        )

    with col5:
        alcohol = st.selectbox(
            "Do you Drink Alcohol?",
            options=["Yes", "No"],
            help="Are you Alcoholic or Not!",
        )

    st.subheader("Health Information:")
    col6, col7, col8, col12 = st.columns(4)

    with col7:
        health_key = st.selectbox(
            "How is your Health?",
            options=[ 'Poor', 'Fair', 'Good', 'Very good', 'Excellent'],
            help="What Would you say that in general your health is!",
        )

    with col12:
        asthma = st.selectbox(
            "Ever had  Asthma?",
            options= ["Yes", "No"],
            help="(Ever told) (you had) Asthma?",
        )
    with col8:
        diabetic = st.selectbox(
            "Are you Diabetic?",
            options= ['Yes', 'No', 'No, borderline diabetes', 'Yes (during pregnancy)'],
            help = "Ever had diabetes?",
        )
    with col6:
        bmi_key = st.selectbox(
            "BMI",
            options= ['UnderWeight', 'NormalWeight', 'OverWeight', 'Obesity Class I', "Obesity Class II", "Obesity Class III"],
            help = "Please choose respective BMI category!",
        )

    st.subheader("Critical Health Issues:")
    col8, col9, col10 = st.columns(3)

    with col8:
        stroke = st.selectbox(
            "Ever had a Heart Stroke in the Past?",
            options=["Yes", "No"],
            help="Ever had a stroke in the past atleast once?",
        )

    with col9:
        skincancer = st.selectbox(
            "Ever Diagnosed with Skin Cancer?",
            options=["Yes", "No"],
            help="(Ever told) Diagnosed with Skin Cancer?",
        )
    with col10:
        kidneydisease = st.selectbox(
            "Ever Diagnosed with Kidney Disease?",
            options=["Yes", "No"],
            help="Not including Kidney Stones, Bladder Infection or Incontinence, were you ever told you had Kidney Disease?",
        )

    st.title("")
    food = None
    exercise = None
    if (health_key == "Poor" or health_key == "Fair"):
        st.markdown("Please select from below dropdown")
        food_habits = ["junk", "greens", "fibre rich", "protein", "balanced diet"]
        exe = ["I exercise regularly", "I exercise few days a week", "I do not exercise"]
        food = st.selectbox("food Habits", food_habits)
        exercise = st.selectbox("Physical Activity", exe)
    col8, col9, col10 = st.columns(3)
    with col8:
        predict = st.button("Predict my Heart Condition!")
                    # with col2:
    # st.title("")

    log_model = pickle.load(open(MODEL_PATH, "rb"))


    if predict:
        st.session_state.predict = True
        if st.session_state.predict:
            df = featuresTransformations_to_df(agecat_key, bmi_key, gender, race, smoking, alcohol, health_key, diabetic, asthma, stroke, skincancer, kidneydisease)
            # df_to_cal = featuresTransformations_to_df(agecat_key, bmi_key, gender, race, smoking, alcohol, health_key, diabetic, asthma, stroke, skincancer, kidneydisease)
            # df.to_csv("data/df.csv")
            ############ commented for API call
            prediction = log_model.predict(df)
            prediction_prob = log_model.predict_proba(df)
            likelihood = (100*(prediction_prob[0][1]/prediction_prob[0][0]))
            percentage = (100*prediction_prob[0][1]).round(0)
            # st.write(f"Model Prediction {prediction} and its probability {prediction_prob}")
            #############

            # url_p = "http://localhost:8000/get_predictions"

            ########
            # Send a POST request to the API
            # response = requests.post(endpoint, files={'data': df.to_csv(index=False)})
            # prediction = response.json().get("prediction")
            # percentage = response.json().get("percentage")
            ########
            if prediction ==0:
                st.subheader(f"You are Healthy💕! - Dr. RandomForest.")
                st.write(f"You are LESS prone to Heart Disease as the probability of Heart Disease in you is {percentage}%.")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("![Good](https://media.giphy.com/media/trhFX3qdAPF3GjYPMt/giphy.gif)")

            else:
                st.subheader("You are not Healthy 😐, better go for a checkup - Dr. RandomForest.")
                st.write(f"You are Highly prone to Heart Disease as the probability of Heart Disease in you is {percentage}% 😲.")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("![Bad](https://media4.giphy.com/media/zaMldSPOkLNu9iYgZ6/giphy.gif?cid=29caca75yzsr24jwjoy2f8ze5azrdqka0mlt7untywajjgme&rid=giphy.gif&ct=g)")



            st.markdown("------------------------------------------------------------------------------")
            st.header("Interpreting the result")
            shap.initjs()
            filename = path+"/model/rf_model_to_predict_heartDisease"
            with open(filename, 'rb') as f:
                model = pickle.load(f)
            # df_test = pd.read_csv("data/test_dataset.csv")
            # df_test = df_test.drop(df_test.columns[0], axis=1)
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(df)

            # shap.plots.force(explainer.expected_value[1], shap_values[1], df)
            # Call the function to plot

            ##renaming columns
            col_names = {"GenHealth": "General_Health","KidneyDisease":"Kidney_Disease","Diabetic_Yes":"Diabetic","SkinCancer":"Skin_Cancer","AgeCategory":"Age","AlcoholDrinking":"Alcoholic"}

            df = df.rename(columns=col_names)

            st_shap(shap.force_plot(explainer.expected_value[1], shap_values[1], df))
            shap_df = pd.DataFrame(shap_values[1]) ##shap values are 2d array in which 1st position has shap values of heart disease(YES)
            shap_df.columns = df.columns
            # Shap Values to a DataFrame

            tdf = shap_df.T
            tdf = tdf.reset_index()
            tdf.columns = ['features', 'shap_values']
            # tdf['abs_ShapValues'] = abs(tdf['shap_values'])
            tdf = tdf.sort_values('shap_values', ascending=False).reset_index(drop=True)
            tdf
            causing_heartdisease = tdf["features"].unique().tolist()[:3]
            t = tdf["features"].unique().tolist()
            st.markdown('<p style="color:black;font-size:30px">Top 3 factors indicating that they have the strongest impact on the model prediction:</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:white;font-size:25px">1. {causing_heartdisease[0]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:white;font-size:25px">2. {causing_heartdisease[1]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:white;font-size:25px">3. {causing_heartdisease[2]}</p>', unsafe_allow_html=True)

            st.markdown(
                '<p style="color:black;font-size:30px">Three factors that are reducing the chances of heart disease for you:</p>',
                unsafe_allow_html=True)
            st.markdown(f'<p style="color:white;font-size:25px">1. {t[-1]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:white;font-size:25px">2. {t[-2]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:white;font-size:25px">3. {t[-3]}</p>', unsafe_allow_html=True)
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown(
                '<p style="color:black;font-size:30px">Here is what you can do to improve your heart health!</p>',
                unsafe_allow_html=True)

            if "General_Health" in causing_heartdisease:

                with st.expander("To Improve General Health"):
                    if food !="":
                        res_food = get_answers_to_ques(f"my diet includes lot of {food} on regular basis, and {exercise}, How to improve general health and reduce the risk of heart disease? ")
                        st.write(res_food)
                    if food == "":
                        res_no_food = get_answers_to_ques(
                            f"How to improve general health and reduce the risk of heart disease? ")
                        st.write(res_no_food)
            if "Kidney_Disease" in causing_heartdisease:
                with st.expander("Kidney Disease"):
                    res_kidney = get_answers_to_ques("What is the effect of kidney disease on heart disease and how to get rid of kidney disease")
                    st.markdown(res_kidney)
            if "Stroke" in causing_heartdisease:
                with st.expander("Stroke"):
                    res_stroke = get_answers_to_ques("I already got a heart stroke and what can be done to avoid heart strokes in future. help me with detailed precautions")
                    st.markdown(res_stroke)
            if "Diabetic" in causing_heartdisease:
                with st.expander("If Diabetic"):
                    st.write("""Diabetes is a well-known risk factor for heart disease, and having diabetes can increase the risk of developing heart disease. This is because high blood sugar levels over time can damage blood vessels and increase the risk of atherosclerosis, which is the build-up of plaque in the arteries.
                    Therefore, it is important for individuals with diabetes to manage their blood sugar levels and other risk factors for heart disease through lifestyle changes, such as maintaining a healthy diet, engaging in regular exercise, and quitting smoking if they smoke.""")
            if "BMI" in causing_heartdisease:
                with st.expander("BMI"):
                    bmi_categories = ['Underweight', 'Normal weight', 'Overweight', 'Obesity class I',
                                      'Obesity class II', 'Obesity class III']
                    bmi_ranges = ['<18.5', '18.5-24.9', '25-29.9', '30-34.9', '35-39.9', '≥40']

                    bmi_df = pd.DataFrame({'BMI Category': bmi_categories, 'BMI Range': bmi_ranges})
                    st.write(bmi_df)
                    st.write("""To stay healthy and reduce the risk of heart disease, it is important to check your BMI and ensure that it falls within the appropriate category. Please refer to the BMI table to determine your category.""")
            if "Alcoholic" in causing_heartdisease:
                with st.expander("If Alcoholic"):
                    res_alc = get_answers_to_ques(
                        "Does drinking alcohol have effect on causing heart disease? if yes, to what extent?")
                    st.markdown(res_alc)
            if "Smoking" in causing_heartdisease:
                with st.expander("Smoking"):
                    res_smoking = get_answers_to_ques(
                        "what is the effect of smoking on heart disease? How to avoid smoking?")
                    st.markdown(res_smoking)

########################################################################################
def analytics():
    st.image(f"{path}/images/global_interpret.png")

def bmi_calculator():
    # Set the title of the app
    st.title("BMI Calculator")

    # Create two input fields for weight and height
    weight = st.number_input("Enter your weight (in kg)")
    height = st.number_input("Enter your height (in cm)")

    # Create a button to calculate the BMI
    if st.button("Calculate BMI"):
        # Convert height from cm to meters
        height_m = height / 100
        # Calculate the BMI
        bmi = weight / (height_m ** 2)
        # Display the BMI
        st.write(f"Your BMI is {bmi:.2f}")
        # Determine the category and display it
        if bmi < 18.5:
            st.write("You are underweight.")
        elif bmi < 25:
            st.write("You have a normal weight.")
        elif bmi < 30:
            st.write("You are overweight.")
        elif bmi < 35:
            st.write("You are in obesity class I.")
        elif bmi < 40:
            st.write("You are in obesity class II.")
        else:
            st.write("You are in obesity class III.")


if __name__ == '__main__':

    selected_operation = st.sidebar.radio("Select a Operation",  ["Homepage", "Predict Heart Health", "Analytics","BMI Calculator"])

    if selected_operation == "Predict Heart Health":
        st.markdown('')
        predict_heart_disease()

    elif selected_operation == "BMI Calculator":
        bmi_calculator()

    elif selected_operation == "Homepage":
        st.markdown('')
        st.markdown('')
        st.markdown('')
        # col1,col2 = st.columns([1,1])
        # with col1:
        st.markdown('This project is designed to provide an efficient way to comprehend meeting content. By enabling users to upload an audio file of their choice for transcription, they can easily review and analyze meeting transcripts. Additionally, the project allows users to ask questions related to the meeting content, making it a comprehensive tool for extracting useful insights.')
        # with col2:
        lottie_img = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_7mpsnbrj.json")
        st_lottie(
            lottie_img,
            speed=1,
            reverse=False,
            loop=True,
            height="450px",
            width=None,
            key=None,
        )
    else:
        st.markdown('')
        st.markdown('')
        st.markdown('')
        analytics()
