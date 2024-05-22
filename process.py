import joblib
import numpy as np
# Load the model from the file
loaded_stack = joblib.load('models/stacking_model.pkl')


# Define a function to predict using the loaded model for a single input
def predict_single_input(input_data):
    # Reshape the input data if needed
    single_input = input_data.reshape(1, -1)  # Assuming input_data is a numpy array
    # Make predictions
    y_pred_class = loaded_stack.predict(single_input)
    return y_pred_class

def health_Prediction(scaled_age, label_Gender, label_family_history, label_benefits, label_care_options, label_anonymity, label_leave, label_work_interfere):
    input_data = np.array([scaled_age,label_Gender, label_family_history, label_benefits, label_care_options, label_anonymity, label_leave, label_work_interfere])  # Replace value1, value2, ... with actual values
    predicted_class = predict_single_input(input_data)
    return int(predicted_class[0])