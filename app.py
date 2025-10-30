from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load trained RandomForest model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # --- Collect form data ---
            Gender = request.form['Gender']
            Married = request.form['Married']
            Education = request.form['Education']
            Self_Employed = request.form['Self_Employed']
            ApplicantIncome = float(request.form['ApplicantIncome'])
            CoapplicantIncome = float(request.form['CoapplicantIncome'])
            LoanAmount = float(request.form['LoanAmount'])
            Loan_Amount_Term = float(request.form['Loan_Amount_Term'])
            Property_Area = request.form['Property_Area']
            Credit_History = float(request.form['Credit_History'])
            Dependents = request.form['Dependents']

            # --- Encode categorical variables ---
            Gender = 1 if Gender == "Male" else 0
            Married = 1 if Married == "Yes" else 0
            Education = 1 if Education == "Graduate" else 0
            Self_Employed = 1 if Self_Employed == "Yes" else 0

            # One-hot encoding for property area
            Property_Area_Rural = 1 if Property_Area == "Rural" else 0
            Property_Area_Semiurban = 1 if Property_Area == "Semiurban" else 0
            Property_Area_Urban = 1 if Property_Area == "Urban" else 0

            # One-hot encoding for dependents
            Dependents_0 = 1 if Dependents == "0" else 0
            Dependents_1 = 1 if Dependents == "1" else 0
            Dependents_2 = 1 if Dependents == "2" else 0
            Dependents_3plus = 1 if Dependents == "3+" else 0

            # --- Arrange features in correct order ---
            final_features = np.array([[ApplicantIncome,
                                        CoapplicantIncome,
                                        LoanAmount,
                                        Loan_Amount_Term,
                                        Credit_History,
                                        Gender,
                                        Married,
                                        Dependents_0,
                                        Dependents_1,
                                        Dependents_2,
                                        Dependents_3plus,
                                        Education,
                                        Self_Employed,
                                        Property_Area_Rural,
                                        Property_Area_Semiurban,
                                        Property_Area_Urban]])

            # --- Make prediction ---
            prediction = model.predict(final_features)[0]
            prediction_text = "✅ Congratulations! You are Eligible for the Loan." if prediction == 1 \
                              else "❌ Sorry, your Loan Application is Rejected."

            return render_template('predict.html', prediction_text=prediction_text)

        except Exception as e:
            return render_template('predict.html', prediction_text=f"⚠️ Error: {str(e)}")

    return render_template('predict.html')

if __name__ == "__main__":
    app.run(debug=True)
