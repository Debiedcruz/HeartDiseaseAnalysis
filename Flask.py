import pickle
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

"Load the trained model from the pickle file"
with open('heart_disease_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)


@app.route('/')
def index():
    return render_template('index.html')


def encoded_features(form_data):
    encoded_features = {}
    Sex = form_data.get('Sex', '').lower()
    encoded_sex = 1 if Sex == 'male' else 0
    encoded_features['Sex'] = encoded_sex

    encoded_features['BadPhysicalHealthDays'] = form_data.get('PhysicalHealthDays')
    encoded_features['BadMentalHealthDays'] = form_data.get('MentalHealthDays')
    print(type(encoded_features['BadMentalHealthDays']))

    "Encode PhysicalActivities"
    encoded_features['PhysicalActivities'] = 1 if form_data.get('PhysicalActivities', 'No') == 'Yes' else 0

    encoded_features['SleepHours'] = form_data.get('SleepHours')

    "Encode HadAngina"
    encoded_features['HadAngina'] = 1 if form_data.get('HadAngina', 'No') == 'Yes' else 0

    "Encode HadStroke"
    encoded_features['HadStroke'] = 1 if form_data.get('HadStroke', 'No') == 'Yes' else 0

    "Encode HadCOPD"
    encoded_features['HadCOPD'] = 1 if form_data.get('HadCOPD', 'No') == 'Yes' else 0

    "Encode HadKidneyDisease"
    encoded_features['HadKidneyDisease'] = 1 if form_data.get('HadKidneyDisease', 'No') == 'Yes' else 0

    "Encode HadArthritis"
    encoded_features['HadArthritis'] = 1 if form_data.get('HadArthritis', 'No') == 'Yes' else 0

    "Encode HadDiabetes"
    encoded_features['HadDiabetes'] = 1 if form_data.get('HadDiabetes', 'No') == 'Yes' else 0

    "Encode DeafOrHardOfHearing"
    encoded_features['DeafOrHardOfHearing'] = 1 if form_data.get('DeafOrHardOfHearing', 'No') == 'Yes' else 0

    "Encode BlindOrVisionDifficulty"
    encoded_features['BlindOrVisionDifficulty'] = 1 if form_data.get('BlindOrVisionDifficulty', 'No') == 'Yes' else 0

    "Encode DifficultyConcentrating"
    encoded_features['DifficultyConcentrating'] = 1 if form_data.get('DifficultyConcentrating', 'No') == 'Yes' else 0

    "Encode DifficultyWalking"
    encoded_features['DifficultyWalking'] = 1 if form_data.get('DifficultyWalking', 'No') == 'Yes' else 0

    "Encode DifficultyDressingBathing"
    encoded_features['DifficultyDressingBathing'] = 1 if form_data.get('DifficultyDressingBathing', 'No') == 'Yes' else 0

    "Encode DifficultyErrands"
    encoded_features['DifficultyErrands'] = 1 if form_data.get('DifficultyErrands', 'No') == 'Yes' else 0

    "Encode ChestScan"
    encoded_features['ChestScan'] = 1 if form_data.get('ChestScan', 'No') == 'Yes' else 0

    encoded_features['BMI'] = form_data.get('BMI')

    "Encode AlcoholDrinkers"
    encoded_features['AlcoholDrinkers'] = form_data.get('AlcoholDrinkers')

    encoded_features['PneumoVaxEver'] = form_data.get('PneumoVaxEver')

    if 'GeneralHealth' in form_data:
        "If 'GeneralHealth_Excellent' is selected, encode it as 1, else encode as 0"
        encoded_features['GeneralHealth_Excellent'] = 1 if form_data['GeneralHealth'] == 'GeneralHealth_Excellent' else 0
    else:
        "If not selected, encode as 0"
        encoded_features['GeneralHealth_Excellent'] = 0

    if 'GeneralHealth' in form_data:
        # If "GeneralHealth_Fair" is selected, encode it as 1, else encode as 0
        encoded_features['GeneralHealth_Fair'] = 1 if form_data['GeneralHealth'] == 'GeneralHealth_Fair' else 0
    else:
        # If not selected, encode as 0
        encoded_features['GeneralHealth_Fair'] = 0

    if 'GeneralHealth' in form_data:
        # If "GeneralHealth_Good" is selected, encode it as 1, else encode as 0
        encoded_features['GeneralHealth_Good'] = 1 if form_data['GeneralHealth'] == 'GeneralHealth_Good' else 0
    else:
        # If not selected, encode as 0
        encoded_features['GeneralHealth_Good'] = 0

    if 'GeneralHealth' in form_data:
        # If "GeneralHealth_Poor" is selected, encode it as 1, else encode as 0
        encoded_features['GeneralHealth_Poor'] = 1 if form_data['GeneralHealth'] == 'GeneralHealth_Poor' else 0
    else:
        encoded_features['GeneralHealth_Poor'] = 0

    if 'GeneralHealth' in form_data:
        # If "GeneralHealth_Very good" is selected, encode it as 1, else encode as 0
        encoded_features['GeneralHealth_Very good'] = 1 if form_data['GeneralHealth'] == 'GeneralHealth_Very good' else 0
    else:
        # If not selected, encode as 0
        encoded_features['GeneralHealth_Very good'] = 0

    # Check if the 'LastCheckupTime_5 or more years ago' option is selected in the form data
    if 'LastCheckupTime' in form_data:
        # If selected, encode 'LastCheckupTime_5 or more years ago' as 1, else encode as 0
        encoded_features['LastCheckupTime_5 or more years ago'] = 1 if form_data['LastCheckupTime'] == 'LastCheckupTime_5 or more years ago' else 0
    else:
        # If not selected, encode 'LastCheckupTime_5 or more years ago' as 0
        encoded_features['LastCheckupTime_5 or more years ago'] = 0

    if 'LastCheckupTime' in form_data:
        # If selected, encode 'LastCheckupTime_5 or more years ago' as 1, else encode as 0
        encoded_features['LastCheckupTime_Within past 2 years (1 year but less than 2 years ago)'] = 1 if form_data['LastCheckupTime'] == 'LastCheckupTime_Within past 2 years (1 year but less than 2 years ago)' else 0
    else:
        # If not selected, encode 'LastCheckupTime_5 or more years ago' as 0
        encoded_features['LastCheckupTime_Within past 2 years (1 year but less than 2 years ago)'] = 0

    if 'LastCheckupTime' in form_data:
        # If selected, encode 'LastCheckupTime_5 or more years ago' as 1, else encode as 0
        encoded_features['LastCheckupTime_Within past 5 years (2 years but less than 5 years ago)'] = 1 if form_data['LastCheckupTime'] == 'LastCheckupTime_Within past 5 years (2 years but less than 5 years ago)' else 0

    else:
        # If not selected, encode 'LastCheckupTime_5 or more years ago' as 0
        encoded_features['LastCheckupTime_Within past 5 years (2 years but less than 5 years ago)'] = 0

    if 'LastCheckupTime' in form_data:
        # If selected, encode 'LastCheckupTime_5 or more years ago' as 1, else encode as 0
        encoded_features['LastCheckupTime_Within past year (anytime less than 12 months ago)'] = 1 if form_data['LastCheckupTime'] == 'LastCheckupTime_Within past year (anytime less than 12 months ago)' else 0
    else:
        # If not selected, encode 'LastCheckupTime_5 or more years ago' as 0
        encoded_features['LastCheckupTime_Within past year (anytime less than 12 months ago)'] = 0

    if 'RemovedTeeth' in form_data:
        # If selected, encode 'RemovedTeeth_1 to 5' as 1, else encode as 0
        encoded_features['RemovedTeeth_1 to 5'] = 1 if form_data['RemovedTeeth'] == 'RemovedTeeth_1 to 5' else 0
    else:
        # If not selected, encode 'RemovedTeeth_1 to 5' as 0
        encoded_features['RemovedTeeth_1 to 5'] = 0

    if 'RemovedTeeth' in form_data:
        # If selected, encode 'RemovedTeeth_6 or more, but not all' as 1, else encode as 0
        encoded_features['RemovedTeeth_6 or more, but not all'] = 1 if form_data['RemovedTeeth'] == 'RemovedTeeth_6 or more, but not all' else 0
    else:
        # If not selected, encode 'RemovedTeeth_6 or more, but not all' as 0
        encoded_features['RemovedTeeth_6 or more, but not all'] = 0

    if 'RemovedTeeth' in form_data:
        # If selected, encode 'RemovedTeeth_All' as 1, else encode as 0
        encoded_features['RemovedTeeth_All'] = 1 if form_data['RemovedTeeth'] == 'RemovedTeeth_All' else 0
    else:
        # If not selected, encode 'RemovedTeeth_All' as 0
        encoded_features['RemovedTeeth_All'] = 0

    if 'RemovedTeeth' in form_data:
        # If selected, encode 'RemovedTeeth_None of them' as 1, else encode as 0
        encoded_features['RemovedTeeth_None of them'] = 1 if form_data['RemovedTeeth'] == 'RemovedTeeth_None of them' else 0
    else:
        # If not selected, encode 'RemovedTeeth_None of them' as 0
        encoded_features['RemovedTeeth_None of them'] = 0

    if 'SmokerStatus' in form_data:
        # If selected, encode 'SmokerStatus_Current smoker - now smokes every day' as 1, else encode as 0
        encoded_features['SmokerStatus_Current smoker - now smokes every day'] = 1 if form_data['SmokerStatus'] == 'SmokerStatus_Current smoker - now smokes every day' else 0
    else:
        # If not selected, encode 'SmokerStatus_Current smoker - now smokes every day' as 0
        encoded_features['SmokerStatus_Current smoker - now smokes every day'] = 0

    if 'SmokerStatus' in form_data:
        # If selected, encode 'SmokerStatus_Current smoker - now smokes every day' as 1, else encode as 0
        encoded_features['SmokerStatus_Current smoker - now smokes some days'] = 1 if form_data['SmokerStatus'] == 'SmokerStatus_Current smoker - now smokes some days' else 0
    else:
        # If not selected, encode 'SmokerStatus_Current smoker - now smokes every day' as 0
        encoded_features['SmokerStatus_Current smoker - now smokes some days'] = 0

    if 'SmokerStatus' in form_data:
        # If selected, encode 'SmokerStatus_Former smoker' as 1, else encode as 0
        encoded_features['SmokerStatus_Former smoker'] = 1 if form_data['SmokerStatus'] == 'SmokerStatus_Former smoker' else 0
    else:
        # If not selected, encode 'SmokerStatus_Current smoker - now smokes every day' as 0
        encoded_features['SmokerStatus_Former smoker'] = 0

    if 'SmokerStatus' in form_data:
        # If selected, encode 'SmokerStatus_Current smoker - now smokes every day' as 1, else encode as 0
        encoded_features['SmokerStatus_Never smoked'] = 1 if form_data['SmokerStatus'] == 'SmokerStatus_Never smoked' else 0
    else:
        # If not selected, encode 'SmokerStatus_Current smoker - now smokes every day' as 0
        encoded_features['SmokerStatus_Never smoked'] = 0

    if 'AgeCategory' in form_data:
        # If the age category "Age 18 to 24" is selected, encode it as 1, else encode as 0
        encoded_features['AgeCategory_Age 18 to 24'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 18 to 24' else 0
    else:
        # If not selected, encode as 0
        encoded_features['AgeCategory_Age 18 to 24'] = 0

    if 'AgeCategory' in form_data:
        # If the age category "Age 18 to 24" is selected, encode it as 1, else encode as 0
        encoded_features['AgeCategory_Age 25 to 29'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 25 to 29' else 0
    else:
        # If not selected, encode as 0
        encoded_features['AgeCategory_Age 25 to 29'] = 0

    if 'AgeCategory' in form_data:
        # If the age category "Age 18 to 24" is selected, encode it as 1, else encode as 0
        encoded_features['AgeCategory_Age 30 to 34'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 30 to 34' else 0
    else:
        # If not selected, encode as 0
        encoded_features['AgeCategory_Age 30 to 34'] = 0

    if 'AgeCategory' in form_data:
        "If the age category Age 18 to 24 is selected, encode it as 1, else encode as 0"
        encoded_features['AgeCategory_Age 35 to 39'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 35 to 39' else 0
    else:
        # If not selected, encode as 0
        encoded_features['AgeCategory_Age 35 to 39'] = 0

    if 'AgeCategory' in form_data:
        # If the age category "Age 18 to 24" is selected, encode it as 1, else encode as 0
        encoded_features['AgeCategory_Age 40 to 44'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 40 to 44' else 0
    else:
        "If not selected, encode as 0"
        encoded_features['AgeCategory_Age 40 to 44'] = 0

    if 'AgeCategory' in form_data:
        "If the age category Age 18 to 24 is selected, encode it as 1, else encode as 0"
        encoded_features['AgeCategory_Age 45 to 49'] = 1 if form_data['AgeCategory'] == 'Yes' else 0
    else:
        "If not selected, encode as 0"
        encoded_features['AgeCategory_Age 45 to 49'] = 0

    if 'AgeCategory' in form_data:
        "If the age category Age 18 to 24 is selected, encode it as 1, else encode as 0"
        encoded_features['AgeCategory_Age 50 to 54'] = 1 if form_data['AgeCategory'] == 'Yes' else 0
    else:
        "If not selected, encode as 0"
        encoded_features['AgeCategory_Age 50 to 54'] = 0

    if 'AgeCategory' in form_data:
        "If the age category Age 18 to 24 is selected, encode it as 1, else encode as 0"
        encoded_features['AgeCategory_Age 55 to 59'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 55 to 59' else 0
    else:
        "If not selected, encode as 0"
        encoded_features['AgeCategory_Age 55 to 59'] = 0

    if 'AgeCategory' in form_data:
        "If the age category Age 18 to 24 is selected, encode it as 1, else encode as 0"
        encoded_features['AgeCategory_Age 60 to 64'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 60 to 64' else 0
    else:
        "If not selected, encode as 0"
        encoded_features['AgeCategory_Age 60 to 64'] = 0

    if 'AgeCategory' in form_data:
        # If the age category "Age 18 to 24" is selected, encode it as 1, else encode as 0
        encoded_features['AgeCategory_Age 65 to 69'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 65 to 69' else 0
    else:
        # If not selected, encode as 0
        encoded_features['AgeCategory_Age 65 to 69'] = 0

    if 'AgeCategory' in form_data:
        "If the age category Age 18 to 24 is selected, encode it as 1, else encode as 0"
        encoded_features['AgeCategory_Age 70 to 74'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 70 to 74' else 0
    else:
        "If not selected, encode as 0"
        encoded_features['AgeCategory_Age 70 to 74'] = 0

    if 'AgeCategory' in form_data:
        "If the age category Age 18 to 24 is selected, encode it as 1, else encode as 0"
        encoded_features['AgeCategory_Age 75 to 79'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 75 to 79' else 0
    else:
        # If not selected, encode as 0
        encoded_features['AgeCategory_Age 75 to 79'] = 0

    if 'AgeCategory' in form_data:
        # If the age category "Age 18 to 24" is selected, encode it as 1, else encode as 0
        encoded_features['AgeCategory_Age 80 or older'] = 1 if form_data['AgeCategory'] == 'AgeCategory_Age 80 or older' else 0
    else:
        # If not selected, encode as 0
        encoded_features['AgeCategory_Age 80 or older'] = 0

    return encoded_features


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        # Render the form
        return render_template('index.html')
    else:
        form_data = request.form.to_dict()
        encoded_feature = encoded_features(form_data)

        'Print the encoded features'
        print("Encoded Features:", encoded_feature)

        'Create DataFrame'
        data = pd.DataFrame([encoded_feature])

        'Make predictions'
        prediction = loaded_model.predict(data)
        print("Prediction:", prediction)

        'Probability of positive outcome'
        prediction_probability = [f'{prob*100:.0f}' for prob in loaded_model.predict_proba(data)[:, 1]]

        print("Prediction Probability:", prediction_probability)

        return render_template('result.html', prediction=prediction[0], prediction_probability=prediction_probability[0])


if __name__ == '__main__':
    app.run(debug=True)
