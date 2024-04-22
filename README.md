"""
This Flask application loads a trained heart disease prediction model from a pickle file
and provides a web interface for users to input their information and receive predictions
about their likelihood of having heart disease.

The application consists of two main routes:

1. '/' (index): Renders the main page where users can input their information.

2. '/predict' (predict): Handles form submission, encodes the input features, makes predictions
   using the loaded model, and renders the result page with the prediction and probability.

Functions:
- index(): Renders the main page with the input form.
- encoded_features(form_data): Encodes the form data into a format suitable for model input.
- predict(): Handles form submission, makes predictions, and renders the result page.

Modules:
- pickle: Used to load the trained model from a pickle file.
- pandas (as pd): Used for handling data.
- Flask: Used to create the web application and handle requests.
- render_template: Used to render HTML templates for Flask.
- request: Used to access form data submitted with the request.

Global variables:
- loaded_model: Holds the trained heart disease prediction model loaded from 'heart_disease_model.pkl'.

Note: This application assumes the existence of HTML templates 'index.html' and 'result.html' in the
      same directory as this script. These templates are used for rendering the user interface.
"""
