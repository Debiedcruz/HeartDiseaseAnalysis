from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)
model = joblib.load('logistic_regression_model.pkl')  # Load your trained model

@app.route('/')
def index():
    return render_template('index1.html')


@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Retrieving each form input value
        sex = int(request.form['sex'])
        general_health = int(request.form['general_health'])
        physical_health_days = int(request.form['physical_health_days'])
        mental_health_days = int(request.form['mental_health_days'])
        last_checkup_time = int(request.form['last_checkup_time'])  # Assuming numerical input, adjust accordingly
        physical_activities = int(request.form['physical_activities'])
        sleep_hours = int(request.form['sleep_hours'])
        removed_teeth = int(request.form['removed_teeth'])
        had_heart_attack = int(request.form['had_heart_attack'])
        had_angina = int(request.form['had_angina'])
        had_stroke = int(request.form['had_stroke'])
        had_copd = int(request.form['had_copd'])
        had_kidney_disease = int(request.form['had_kidney_disease'])
        had_arthritis = int(request.form['had_arthritis'])
        had_diabetes = int(request.form['had_diabetes'])
        deaf_or_hard_of_hearing = int(request.form['deaf_or_hard_of_hearing'])
        blind_or_vision_difficulty = int(request.form['blind_or_vision_difficulty'])
        difficulty_concentrating = int(request.form['difficulty_concentrating'])
        difficulty_walking = int(request.form['difficulty_walking'])
        difficulty_dressing_bathing = int(request.form['difficulty_dressing_bathing'])
        difficulty_errands = int(request.form['difficulty_errands'])
        smoker_status = int(request.form['smoker_status'])
        chest_scan = int(request.form['chest_scan'])
        age_category = int(request.form['age_category'])
        bmi = float(request.form['bmi'])
        alcohol_drinkers = int(request.form['alcohol_drinkers'])
        pneumovax_ever = int(request.form['pneumovax_ever'])

        
        input_features = [Sex, GeneralHealth, PhysicalHealthDays, MentalHealthDays, LastCheckupTime, PhysicalActivities, SleepHours, RemovedTeeth,	HadHeartAttack,	HadAngina,	HadStroke,	HadCOPD,	HadKidneyDisease,	HadArthritis,	HadDiabetes,	DeafOrHardOfHearing,	BlindOrVisionDifficulty,	DifficultyConcentrating,	DifficultyWalking, DifficultyDressingBathing, DifficultyErrands, SmokerStatus, ChestScan, AgeCategory, BMI, AlcoholDrinkers, PneumoVaxEver]  # Add other features
        input_features = np.array(input_features).reshape(1, -1)
        
        # Predict probabilities
        proba = model.predict_proba(input_features)
        positive_proba = proba[0, 1]  # Probability of the positive class (heart disease)
        percentage = round(positive_proba * 100, 2)  # Convert to percentage
        
        return render_template('result.html', percentage=percentage)

if __name__ == '__main__':
    app.run(debug=True)
