from fastapi.testclient import TestClient
from api_main import app
import requests
client = TestClient(app)

# def test_server_response():
# #     response = requests.get('http://localhost:8000/docs')
#     response = requests.get('http://http://44.215.237.186/docs')
#     assert response.status_code == 200

def test_predict_endpoint():
#     url = 'http://localhost:8000/predict'
    url = 'http://44.215.237.186:8000/predict'
    headers = {'Content-Type': 'application/json'}
    data = {
        "AgeCategory": 1,
        "Stroke": 1,
        "Diabetic_Yes": 1,
        "KidneyDisease": 0,
        "Smoking": 1,
        "SkinCancer": 0,
        "Is_Male": 1,
        "BMI": 1,
        "Asthma": 0,
        "Race_White": 1,
        "AlcoholDrinking": 0,
        "GenHealth": 1
    }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 200
    assert 'value_0' in response.json()
    assert 'value_1' in response.json()

def test_predict_endpoint_422():
#     url = 'http://localhost:8000/predict'
    url = 'http://44.215.237.186:8000/predict'
    headers = {'Content-Type': 'application/json'}
    # Invalid data - missing required field
    data = {
        "Stroke": 1,
        "Diabetic_Yes": 1,
        "KidneyDisease": 0,
        "Smoking": 1,
        "SkinCancer": 0,
        "Is_Male": 1,
        "BMI": 1,
        "Asthma": 0,
        "Race_White": 1,
        "AlcoholDrinking": 0,
        "GenHealth": 1
        }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 422

def test_predict_endpoint_404():
#     url = 'http://localhost:8000/nonexistent_endpoint'
    url = 'http://44.215.237.186:8000/nonexistent_endpoint'
    headers = {'Content-Type': 'application/json'}
    data = {
        "AgeCategory": 1,
        "Stroke": 1,
        "Diabetic_Yes": 1,
        "KidneyDisease": 0,
        "Smoking": 1,
        "SkinCancer": 0,
        "Is_Male": 1,
        "BMI": 1,
        "Asthma": 0,
        "Race_White": 1,
        "AlcoholDrinking": 0,
        "GenHealth": 1
        }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 404

def test_predict_endpoint_500():
#     url = 'http://localhost:8000/predict'
    url = 'http://44.215.237.186:8000/predict'
    headers = {'Content-Type': 'application/json'}
    # Invalid data - value error
    data = {
        "AgeCategory": "invalid",
        "Stroke": 1,
        "Diabetic_Yes": 1,
        "KidneyDisease": 0,
        "Smoking": 1,
        "SkinCancer": 0,
        "Is_Male": 1,
        "BMI": 1,
        "Asthma": 0,
        "Race_White": 1,
        "AlcoholDrinking": 0,
        "GenHealth": 1
        }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 422
