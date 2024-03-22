from flask import Flask, render_template, request

import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the encoded features and the trained model from the pickle file
with open('logistic_regression_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Retrieve form data and make predictions
        prediction = make_prediction(request.form)
        return render_template('result.html', prediction=prediction)
    else:
        # Render the form
        return render_template('index1.html')

def make_prediction(form_data):
    # Extract form data
    Sex = form_data['Sex']
    GeneralHealth = form_data['GeneralHealth']  # No conversion needed for drop-down values
    PhysicalHealthDays = int(form_data['PhysicalHealthDays'])
    MentalHealthDays = int(form_data['MentalHealthDays'])
    LastCheckupTime = form_data['LastCheckupTime']  # No conversion needed for drop-down values
    PhysicalActivities = form_data['PhysicalActivities']
    SleepHours = int(form_data['SleepHours'])
    RemovedTeeth = form_data['RemovedTeeth']
    HadAngina = form_data['HadAngina']
    HadStroke = form_data['HadStroke']
    HadCOPD = form_data['HadCOPD']
    HadKidneyDisease = form_data['HadKidneyDisease']
    HadArthritis = form_data['HadArthritis']
    HadDiabetes = form_data['HadDiabetes']
    DeafOrHardOfHearing = form_data['DeafOrHardOfHearing']
    BlindOrVisionDifficulty = form_data['BlindOrVisionDifficulty']
    DifficultyConcentrating = form_data['DifficultyConcentrating']
    DifficultyWalking = form_data['DifficultyWalking']
    DifficultyDressingBathing = form_data['DifficultyDressingBathing']
    DifficultyErrands = form_data['DifficultyErrands']
    SmokerStatus = form_data['SmokerStatus']  # No conversion needed for drop-down values
    ChestScan = form_data['ChestScan']
    AgeCategory = form_data['AgeCategory']  # No conversion needed for drop-down values
    BMI = float(form_data['BMI'])
    AlcoholDrinkers = form_data['AlcoholDrinkers']
    PneumoVaxEver = form_data['PneumoVaxEver']

    # Prepare input features
    input_features = [Sex, GeneralHealth, PhysicalHealthDays, MentalHealthDays, LastCheckupTime, PhysicalActivities,
                      SleepHours, RemovedTeeth, HadAngina, HadStroke, HadCOPD, HadKidneyDisease, HadArthritis,
                      HadDiabetes, DeafOrHardOfHearing, BlindOrVisionDifficulty, DifficultyConcentrating,
                      DifficultyWalking, DifficultyDressingBathing, DifficultyErrands, SmokerStatus, ChestScan,
                      AgeCategory, BMI, AlcoholDrinkers, PneumoVaxEver]

    # Perform label encoding on categorical features in input_features
    le = LabelEncoder()
    for i, feature in enumerate(input_features):
        if isinstance(feature, str):
            input_features[i] = le.fit_transform([feature])[0]

    # Predict
    predicted_value = model.predict([input_features])[0]

    return predicted_value

if __name__ == '__main__':
    app.run(debug=True)
