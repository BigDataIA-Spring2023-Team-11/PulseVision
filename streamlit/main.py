import io
import json

import pandas as pd
import datetime
import re

import base64
import plotly.express as px

import pickle
# all other imports
import requests
import os
# from streamlit_elements import Elements
import streamlit_shap as st_shap
import streamlit as st
import shap
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# from loginpage import login, registration
from utils import get_answers_to_ques, write_logs_to_cloudwatch, read_register_user_logs

import streamlit as st
import time
import boto3
from dotenv import load_dotenv
import os
import subprocess
import hashlib
import json
import altair as alt

import base64
###############################################################################
load_dotenv()
# The code below is for the layout of the page
if "widen" not in st.session_state:
    layout = "centered"
else:
    layout = "wide" if st.session_state.widen else "centered"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'predict' not in st.session_state:
    st.session_state.predict = False

# Create a CloudWatch Logs client
# Set all credentials and variables
aws_access_key_id = os.getenv('ACCESS_KEY')
aws_secret_access_key = os.getenv('SECRET_KEY')

client = boto3.client('logs',region_name="us-east-1",
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

# Define the CloudWatch Logs group and log stream name
log_group_name = 'pulse-vision-logs'
log_stream_name = 'registration-logs'

# Define a variable to hold the logged in user's details
logged_in_user = None

path = os.path.dirname(__file__)




def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
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
image_file = path+'/images/white_gred.jpeg'

# Image from link
# add_bg_from_local(bgimage_link)

# Model Path
MODEL_PATH = path+"/model/model"

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
    st.title("PULSE VISION")
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
            help = """Please choose respective BMI category! 
            
            BMI < 18.5 ---> UnderWeight'
            18.5 <= BMI <= 25 ---> NormalWeight'
            25 <= BMI <= 30 ---> OverWeight'
            30 <= BMI <= 35 ---> Obesity Class I'
            35 <= BMI <= 40 ---> Obesity Class II'
            40 <= BMI ---> Obesity Class III'
                    
            """,
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
        st.subheader("Please select from below dropdown")
        food_habits = ["junk", "greens", "fibre rich", "protein", "balanced diet"]
        exe = ["I exercise regularly", "I exercise few days a week", "I do not exercise"]
        food = st.selectbox("Food Habits", food_habits)
        exercise = st.selectbox("Physical Activity", exe)
    col8, col9, col10 = st.columns(3)
    with col8:
        predict = st.button("Predict my Heart Condition!")

    colored_red = f"<span style='color:red'>RED</span>"
    colored_blue = f"<span style='color:blue'>BLUE</span>"

    def bar_char_altair(df, color):
        # Create the chart
        df = df.sort_values(by= "% Contribution", ascending=False).reset_index(drop=True)

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('features', sort='-y'),
            y=alt.Y("% Contribution", axis=alt.Axis(format=',.0f', title='Value')),
            color=alt.condition(
                alt.datum.Value > 0,
                alt.value('red'),  # Positive values will be green
                alt.value(color)  # Negative values will be red
            )
        ).properties(width=600, height=00)
        return chart



    if predict:
        st.session_state.predict = True
        if st.session_state.predict:
            df = featuresTransformations_to_df(agecat_key, bmi_key, gender, race, smoking, alcohol, health_key, diabetic, asthma, stroke, skincancer, kidneydisease)
            #############

            # url_p = "http://localhost:8000/get_predictions"

            ########
            # Send a POST request to the API
            payload = json.dumps({
                "AgeCategory": int(df.AgeCategory[0]),
                "Stroke": int(df.Stroke[0]),
                "Diabetic_Yes": int(df.Diabetic_Yes[0]),
                "KidneyDisease": int(df.KidneyDisease[0]),
                "Smoking": int(df.Smoking[0]),
                "SkinCancer": int(df.SkinCancer[0]),
                "Is_Male": int(df.Is_Male[0]),
                "BMI": int(df.BMI[0]),
                "Asthma": int(df.Asthma[0]),
                "Race_White": int(df.Race_White[0]),
                "AlcoholDrinking": int(df.AlcoholDrinking[0]),
                "GenHealth": int(df.GenHealth[0])
            })
            # st.markdown(payload)
            headers = {
                'Content-Type': 'application/json'
            }
            url = f"{endpoint}"
            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                json_data = json.loads(response.text)
                # st.json(json_data)

                prediction = response.json().get("prediction")
                percentage = response.json().get("prediction_probability")
                if prediction == 0:
                    st.subheader(f"You are Healthy💕! - Dr. RandomForest.")
                    st.info(
                        f"You are LESS prone to Heart Disease as the probability of Heart Disease in you is {percentage}%.")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("![Good](https://media.giphy.com/media/trhFX3qdAPF3GjYPMt/giphy.gif)")

                else:
                    st.subheader("You are not Healthy 😐, better go for a checkup - Dr. RandomForest.")
                    st.warning(
                        f"You are Highly prone to Heart Disease as the probability of Heart Disease in you is {percentage}% 😲.")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(
                            "![Bad](https://media4.giphy.com/media/zaMldSPOkLNu9iYgZ6/giphy.gif?cid=29caca75yzsr24jwjoy2f8ze5azrdqka0mlt7untywajjgme&rid=giphy.gif&ct=g)")


            else:
                st.text("Invalid Inputs ⚠️")
            # ########



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
            # st_shap(shap.plots.waterfall(explainer.expected_value[1], shap_values[1]), height=300)

            st.markdown(
                f"""***Graph Represents Impact of each Feature on the Heart Disease Prediction:***\n1. Features Highlighted in **{colored_red}** indicate an **Increase** in their Impact on Heart Disease.\n2. Features Highlighted in **{colored_blue}** indicate a **Decrease** in their Impact on Heart Disease.\n3. **Longer** bars indicate a **Greater Impact** on Heart Disease, and **Arrows** show the **Direction of the Impact**.\n4. Features are ordered based on their overall Impact.
            """, unsafe_allow_html=True)
            shap_df = pd.DataFrame(shap_values[1]) ##shap values are 2d array in which 1st position has shap values of heart disease(YES)
            shap_df.columns = df.columns
            # Shap Values to a DataFrame
            st.markdown("")
            tdf = shap_df.T
            tdf = tdf.reset_index()
            tdf.columns = ['features', 'shap_values']
            # tdf['abs_ShapValues'] = abs(tdf['shap_values'])
            tdf = tdf.sort_values('shap_values', ascending=False).reset_index(drop=True)
            tdf["% Contribution"] = abs(tdf["shap_values"] / abs(tdf["shap_values"]).sum() * 100)
            # tdf
            # All Positive impact features
            positive_chart = bar_char_altair(tdf[tdf.shap_values > 0].iloc[:3,:], '#f21365')
            # All Negative impact features
            negative_chart = bar_char_altair(tdf[tdf.shap_values < 0].iloc[-3:, :], '#1e8ce6')

            # Display the chart in Streamlit
            st.subheader("Top features that have Positive Impact: (Increasing the Chances of Heart Disease)")
            st.altair_chart(positive_chart, use_container_width=True)

            st.subheader("Top features that have Negative Impact: (Reducing the Chances of Heart Disease)")
            st.altair_chart(negative_chart, use_container_width=True)
            top_features = tdf[tdf.shap_values > 0]["features"].unique().tolist()
            st.subheader("Top 3 factors indicating that they have the Strongest Impact on the Heart Disease")
            features_cant_change = ["Race_White","Is_Male","Age"]
            for feature in top_features[:3]:
                if feature not in features_cant_change:
                    st.markdown(f'<p style="color:red;font-size:25px">- {feature}</p>',
                            unsafe_allow_html=True)
            st.markdown("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

            st.markdown(
                '<p style="color:black;font-size:30px">Here is what you can do to improve your heart health!</p>',
                unsafe_allow_html=True)

            if "General_Health" in top_features[:3]:

                with st.expander("To Improve General Health"):
                    if food !="":
                        res_food = get_answers_to_ques(f"my diet includes lot of {food} on regular basis, and {exercise}, How to improve general health and reduce the risk of heart disease? ")
                        st.write(res_food)
                    if food == "":
                        res_no_food = get_answers_to_ques(
                            f"How to improve general health and reduce the risk of heart disease? ")
                        st.write(res_no_food)
            if "Kidney_Disease" in top_features[:3]:
                with st.expander("Kidney Disease"):
                    res_kidney = get_answers_to_ques("What is the effect of kidney disease on heart disease and how to get rid of kidney disease")
                    st.markdown(res_kidney)
            if "Stroke" in top_features[:3]:
                with st.expander("Stroke"):
                    res_stroke = get_answers_to_ques("I already got a heart stroke and what can be done to avoid heart strokes in future. help me with detailed precautions")
                    st.markdown(res_stroke)
            if "Diabetic" in top_features[:3]:
                with st.expander("If Diabetic"):
                    st.write("""Diabetes is a well-known risk factor for heart disease, and having diabetes can increase the risk of developing heart disease. This is because high blood sugar levels over time can damage blood vessels and increase the risk of atherosclerosis, which is the build-up of plaque in the arteries.
                    Therefore, it is important for individuals with diabetes to manage their blood sugar levels and other risk factors for heart disease through lifestyle changes, such as maintaining a healthy diet, engaging in regular exercise, and quitting smoking if they smoke.""")
            if "BMI" in top_features[:3]:
                with st.expander("BMI"):
                    bmi_categories = ['Underweight', 'Normal weight', 'Overweight', 'Obesity class I',
                                      'Obesity class II', 'Obesity class III']
                    bmi_ranges = ['<18.5', '18.5-24.9', '25-29.9', '30-34.9', '35-39.9', '≥40']

                    bmi_df = pd.DataFrame({'BMI Category': bmi_categories, 'BMI Range': bmi_ranges})
                    st.write(bmi_df)
                    st.write("""To stay healthy and reduce the risk of heart disease, it is important to check your BMI and ensure that it falls within the appropriate category. Please refer to the BMI table to determine your category.""")
            if "Alcoholic" in top_features[:3]:
                with st.expander("If Alcoholic"):
                    res_alc = get_answers_to_ques(
                        "Does drinking alcohol have effect on causing heart disease? if yes, to what extent?")
                    st.markdown(res_alc)
            if "Smoking" in top_features[:3]:
                with st.expander("Smoking"):
                    res_smoking = get_answers_to_ques(
                        "what is the effect of smoking on heart disease? How to avoid smoking?")
                    st.markdown(res_smoking)
            if "Asthma" in top_features[:3]:
                with st.expander("Asthma"):
                    res_asth = get_answers_to_ques(
                        "How to get rid of asthma to prevent heart disease?")
                    st.markdown(res_asth)

########################################################################################
def Insights():
    st.image(f"{path}/images/global_interpret.png")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.subheader(
        f"""***Graph Represents Impact of each Feature on the Heart Disease Prediction:***""")
    st.markdown("""
    - One of the most significant factors is age, with older people having a higher risk than younger people
    
- Poor general health, a history of stroke, kidney disease,Skin cancer, Asthma and diabetes can also increase the likelihood of developing heart disease

- Gender is also a factor, with men being at higher risk than women. However, it's important to note that these factors don't guarantee that someone will develop heart disease, but they do increase the probability

- In terms of alcohol consumption, moderate drinking can have some protective effects on the heart and circulatory system, but heavy drinking can be harmful and is a major cause of preventable death

 Understanding these factors and their relationships can help individuals make informed decisions about their lifestyle choices and healthcare providers identify individuals who may be at higher risk of heart disease. By taking appropriate measures, such as adopting a healthier lifestyle, managing chronic conditions like diabetes, and seeking medical treatment if necessary, individuals can reduce their risk of developing heart disease.
    """)

def bmi_calculator():
    # Set the title of the app
    st.title("BMI Calculator")

    # Create two input fields for weight and height
    weight = st.number_input("Enter your weight (in kg)")
    height = st.number_input("Enter your height (in cm)")

    # st.markdown(f"{height} --> {type(height)} --> {height > }")
    # Create a button to calculate the BMI
    if st.button("Calculate BMI"):
        if int(height) <= 0 & int(weight) <= 0:
            st.error("Please Provide Valid Information!.")
        else:
            # if height.astype('float') > 0 & weight.astype('float') > 0:
            # Convert height from cm to meters
            height_m = height / 100
            # Calculate the BMI
            bmi = weight / (height_m ** 2)
            # Display the BMI
            st.write(f"Your BMI is {bmi:.2f}")
            # Determine the category and display it
            if bmi < 18.5:
                st.info("You are underweight.")
            elif bmi < 25:
                st.info("You have a normal weight.")
            elif bmi < 30:
                st.info("You are overweight.")
            elif bmi < 35:
                st.info("You are in obesity class I.")
            elif bmi < 40:
                st.info("You are in obesity class II.")
            else:
                st.info("You are in obesity class III.")

    # Define a function to get the log events from CloudWatch
def get_log_events():
    end_time = int(datetime.datetime.now().timestamp()) * 1000
    start_time = int((datetime.datetime.now() - datetime.timedelta(days=5)).timestamp()) * 1000

    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        # startTime=start_time,
        # endTime=end_time
        startFromHead=True
    )

    log_events = []
    for event in response['events']:
        message = event['message']
        log_events.append(message)

    st.markdown(f"{len(log_events)} --> {log_events} ---> log events")

    # dict_ = dict(item.split("=") for item in string.split(", "))
    #
    # # Convert the dictionary to a dataframe
    # df = pd.DataFrame(dict_, index=[0])[["name", "email", "password_hash"]]
    #
    # df = pd.DataFrame([m.split('///') for m in messages], columns=['email', 'username', 'password', 'plan'])
    # df['timestamp'] = pd.to_datetime(timestamps, unit='ms')

    return log_events

def registration():
    st.markdown(
        "<h3 style='text-align: center'><span style='color: #2A76BE;'>Registration Page</span></h3>",
        unsafe_allow_html=True)

    with st.form("Registration Form"):
        # Get user details
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')

        # Hash the password using SHA-256
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        submit_button = st.form_submit_button(label="Register")

        if submit_button:
            # if name.strip() == "" or email.strip() == "" or password.strip() == "" or confirm_password.strip() == "":
            #     st.error("Please fill out all fields")
            # elif password != confirm_password:
            #     st.error('Passwords do not match')
            # else:
            #     # Check if user already exists
            #     user_exists = check_if_user_exists(email)
            #
            #     if user_exists == "exists":
            #         st.error('User with this email already exists')
            #     else:
            #         # Save user details to database
            #         write_logs_to_cloudwatch(f"{name}###{email}###{password_hash}","registration-logs")
            #         # save_user_details(name, email, password_hash)
            #         st.success('Registration successful')
#     ----------------------- Commented for using other logic
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            password_regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[a-zA-Z\d@$!%*?&]{5,}$"
            user_exists = check_if_user_exists(email)

            if re.match(email_regex, email) == None:
                st.error("Please enter valid Email")
            elif user_exists == 'exists':
                st.error("User Already Exists")
            elif password != confirm_password:
                st.error('Passwords do not Match')
            elif re.match(password_regex, password) == None:
                st.error('Please enter valid Password (Length of at least 5, at least 1 Uppercase Letter and 1 Number)')
            elif (name != "" and password != "" and email != "" and confirm_password != ""):
                write_logs_to_cloudwatch(f"{name}###{email}###{password_hash}", "registration-logs")
                # save_user_details(name, email, password_hash)
                st.success('Registration successful')

                #
                # # username_unique_flag = check_username_doesnot_exists(username)
                # # st.markdown(f"USERNAME Unique --> {username_unique_flag}")
                # # Validate each email address before inserting it into the table
                # # for row in data:
                # #     email = row[0]
                #
                # if user_exists == 'not_exists':
                #     # Save user details to database
                #
                #
                # else:
                #     st.error(f"User Already Exists!")


            else:
                st.info("Please Provide Valid Credentials")


# def check_user_exists(email):
#     # Retrieve the log events from CloudWatch
#     user_credentials = get_user_details(email)
#     if email == user_credentials["email"]:
#         return True
#     return False



def check_if_user_exists(email):
    df = read_register_user_logs()
    # st.markdown(df)
    if email in df.email.unique().tolist():
        return "exists"
    else:
        return "not_exists"

def save_user_details(name, email, password_hash):
    # Save user details to CloudWatch Logs
    message = f'New user registered: name={name}, email={email}, password_hash={password_hash}'
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[
            {
                'timestamp': int(time.time() * 1000),
                'message': message
            }
        ]
    )

# Create a function for the login page
def login():
    st.markdown(
        "<h3 style='text-align: center'><span style='color: #2A76BE;'>Login Page</span></h3>",
        unsafe_allow_html=True)

    # Get user details
    username = st.text_input("Email")
    password = st.text_input("Password", type='password')

    # Hash the password entered by the user
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Login user on form submission
    if st.button('Login'):
        # Validate user credentials
        if username != "" and password != "":

            df = read_register_user_logs()
            # st.markdown(df[df.email == username].shape[0])
            if df[df.email == username].shape[0] > 0:
                # st.markdown(f"{df[df.email == username]['password'][0]} --> {df[df.email == username]['password']} --> {len(df[df.email == username]['password'].tolist())}")
                # st.dataframe(df[df.email == username])
                # st.markdown(df[df.email == username]['password'].tolist()[0])
                pwd = df[df.email == username]['password'].tolist()[0]
                if pwd == password_hash:
                    st.success("Valid Credentials, User logged in!")
                    st.session_state.logged_in = True
                    #     st.session_state.logged_in_user = logged_in_user
                else:
                    st.error("Username does not exist!")
            else:
                st.error("Invalid User!")
        # user_credentials = validate_credentials(username, password_hash)
        # if user_credentials is not None:
        #     user = get_user_details(username)
        #     global logged_in_user
        #     logged_in_user = {"email": user["email"], "name": user["name"]}
        #     print(f" in login : {logged_in_user}")
        #     st.success('Login successful')
        #     st.session_state.logged_in = True
        #     st.session_state.logged_in_user = logged_in_user
        #     message = f'User login success: username={username}'
        #     response = client.put_log_events(
        #         logGroupName=log_group_name,
        #         logStreamName="login-logs",
        #         logEvents=[
        #             {
        #                 'timestamp': int(time.time() * 1000),
        #                 'message': message
        #             }
        #         ]
        #     )

        else:
            st.error('Invalid username or password')
            # message = f'User login failed: username={username}'
            # # response = client.put_log_events(
            # #     logGroupName=log_group_name,
            # #     logStreamName="login-logs",
            # #     logEvents=[
            # #         {
            # #             'timestamp': int(time.time() * 1000),
            # #             'message': message
            # #         }
            # #     ]
            # # )

def get_user_details(username):
    log_events = get_log_events()

    # Parse the log events to extract the relevant user credentials
    st.markdown(f"{len(log_events)} --> {log_events} ---> log events")
    user_credentials = {}
    for log_event in log_events:
        if 'New user registered' in log_event:
            cred = log_event.split(", ")
            email = cred[1].split("=")
            st.markdown(f"{cred},{email}-------------------??????")
            if email[1] == username:
                credentials = log_event.split(': ')[1]
                credentials = credentials.split(', ')
                for credential in credentials:
                    key, value = credential.split('=')
                    user_credentials[key] = value
    st.markdown(f"{user_credentials}-------> credentials")
    return user_credentials

# Define a function to validate the login credentials
def validate_credentials(username, password_hash):
    user_credentials = get_user_details(username)
    # Check if the provided credentials match the registered user credentials
    if username == user_credentials['email'] and password_hash == user_credentials['password_hash']:
        return user_credentials
    else:
        return None

if __name__ == '__main__':

    selected_operation = st.sidebar.radio("Select a Operation",
                                          ["Login", "Registration", "Homepage", "Predict Heart Health", "Insigths",
                                           "BMI Calculator"])

    if selected_operation == "Logout":
        st.session_state.logged_in = False
        st.experimental_set_query_params(logged_in=False)
        st.success("Logged out successfully")
    elif selected_operation == "Login":
        if st.session_state.logged_in:
            st.markdown("Active User Found!")
        else:
            st.session_state.logged_in = False
            login()
    elif selected_operation == "Registration":
        if st.session_state.logged_in:
            st.success("Active User Found!")
        else:
            st.session_state.logged_in = False
            registration()

    # Lets say a USER Logged-In
    if st.session_state.logged_in:
        lo_btn = st.sidebar.button("Logout")
        if selected_operation == "Predict Heart Health":
            st.markdown('')
            predict_heart_disease()

        elif selected_operation == "BMI Calculator":
            bmi_calculator()

        elif selected_operation == "Homepage":
            st.title("PULSE VISION")
            st.markdown("""Pulse Vision is an essential tool for anyone who wants to maintain or improve their heart health. Heart disease is one of the leading causes of death worldwide, and many risk factors for heart disease can be managed or even prevented through lifestyle changes. However, it can be difficult to know where to start, and many people may not realize the impact that their daily habits have on their heart health.""")
            st.markdown("""That's where Pulse Vision comes in. By providing a simple and intuitive way to assess heart-disease risk and track progress over time, the app empowers individuals to take charge of their heart health. With personalized recommendations based on individual risk factors and lifestyle habits, users can make informed decisions about their health and take proactive steps towards a healthier heart.""")
            # with col2:
            lottie_img = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_GZVTNZ.json")
            st_lottie(
                lottie_img,
                speed=1,
                reverse=False,
                loop=True,
                height="450px",
                width=None,
                key=None,
            )

        elif selected_operation == 'Insigths':
            st.title('Global Interpretation')
            Insights()


        if lo_btn:
            st.success("User Logged-out Successfully!")
            st.session_state.logged_in = False

    else:
        st.warning("Please Log-In to get access")