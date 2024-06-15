from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = Flask(__name__)

# Load the pre-trained model
model_filename1 = 'models/random_forest_model.pkl'
with open(model_filename1, 'rb') as file:
    model_random = pickle.load(file)

# Load the label encoders
model_filename2 = 'models/label_encoder.pkl'
with open(model_filename2, 'rb') as f:
    label_encoders = pickle.load(f)

# Load the standard scaler
model_filename3 = 'models/standard_scaler.pkl'
with open(model_filename3, 'rb') as f:
    scaler = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input values from the form
    international_plan = request.form['international_plan']
    voice_mail_plan = request.form['voice_mail_plan']
    account_length = int(request.form['account_length'])
    number_vmail_messages = float(request.form['number_vmail_messages'])
    total_day_minutes = float(request.form['total_day_minutes'])
    total_day_calls = float(request.form['total_day_calls'])
    total_eve_minutes = float(request.form['total_eve_minutes'])
    total_eve_calls = float(request.form['total_eve_calls'])
    total_night_minutes = float(request.form['total_night_minutes'])
    total_night_calls = float(request.form['total_night_calls'])
    total_intl_minutes = float(request.form['total_intl_minutes'])
    total_intl_calls = float(request.form['total_intl_calls'])
    customer_service_calls = float(request.form['customer_service_calls'])
    
    # Perform label encoding on the categorical columns
    label_encoder = LabelEncoder()
    international_plan = label_encoder.fit_transform([international_plan])[0]
    voice_mail_plan = label_encoder.fit_transform([voice_mail_plan])[0]
    
    # Create a DataFrame with the input values
    input_df = pd.DataFrame({
        'International plan': [international_plan],
        'Voice mail plan': [voice_mail_plan],
        'Account length': [account_length],
        'Number vmail messages': [number_vmail_messages],
        'Total day minutes': [total_day_minutes],
        'Total day calls': [total_day_calls],
        'Total eve minutes': [total_eve_minutes],
        'Total eve calls': [total_eve_calls],
        'Total night minutes': [total_night_minutes],
        'Total night calls': [total_night_calls],
        'Total intl minutes': [total_intl_minutes],
        'Total intl calls': [total_intl_calls],
        'Customer service calls': [customer_service_calls]
    })

    # Perform scaling on the numerical columns
    numerical_cols = ['Account length', 'Number vmail messages', 'Total day minutes', 'Total day calls',
                      'Total eve minutes', 'Total eve calls', 'Total night minutes', 'Total night calls',
                      'Total intl minutes', 'Total intl calls', 'Customer service calls']
    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])

    # Make predictions using the pre-trained model
    prediction = model_random.predict(input_df)
    #print(churn_prediction)

    
    return render_template('index.html', prediction=prediction[0])


if __name__ == '__main__':
    app.run(debug=True)
