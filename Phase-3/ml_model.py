import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load health data from Firestore or a CSV
def load_health_data():
    data = {
        'BMI': [22.5, 27.4, 31.1, 24.3, 29.0, 25.5],
        'heart_rate': [72, 85, 90, 65, 78, 80],
        'systolic_bp': [120, 140, 130, 125, 135, 128],
        'diastolic_bp': [80, 90, 85, 78, 88, 82],
        'age': [25, 45, 52, 30, 39, 41],
        'hypertension_risk': [0, 1, 1, 0, 1, 0]  # Target variable
    }
    df = pd.DataFrame(data)
    return df

# Preprocess data
df = load_health_data()
X = df[['BMI', 'heart_rate', 'systolic_bp', 'diastolic_bp', 'age']]
y = df['hypertension_risk']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'hypertension_risk_model.pkl')

# Define detailed recommendations
def get_detailed_recommendations(risk_level):
    recommendations = {
        0: {  # Low Risk
            "Proteins": [
                "Lean chicken breast, Fish (salmon, mackerel, tuna), Eggs, Greek yogurt, Tofu, Lentils"
            ],
            "Food Items": [
                "Leafy greens (spinach, kale), Berries (blueberries, strawberries), Whole grains (brown rice, quinoa), Almonds, Walnuts, Olive oil"
            ],
            "Exercise": [
                "30-45 minutes of moderate exercise, 5 days a week. Options: brisk walking, cycling, swimming, or strength training",
                "Include flexibility exercises, like yoga or stretching, 1-2 times a week"
            ],
            "Mental Wellness": [
                "Practice mindfulness meditation for 10 minutes a day to reduce stress.",
                "Consider journaling to manage thoughts and emotions effectively."
            ],
            "Hydration": [
                "Drink at least 8-10 glasses of water daily; increase intake with physical activity or hot weather.",
                "Avoid sugary drinks and excessive caffeine."
            ],
            "Sleep Hygiene": [
                "Aim for 7-8 hours of sleep per night.",
                "Establish a regular sleep schedule and avoid screens 1 hour before bed."
            ],
        },
        1: {  # High Risk
            "Proteins": [
                "Skinless poultry, Low-fat dairy, Plant-based proteins (beans, lentils, chickpeas), Soy milk"
            ],
            "Food Items": [
                "High-fiber vegetables (broccoli, carrots), Low-sodium options, Foods rich in potassium (bananas, sweet potatoes, avocados), Avoid processed foods"
            ],
            "Exercise": [
                "20-30 minutes of light to moderate exercise, 3-5 days a week. Options: gentle walking, swimming, light resistance training",
                "Focus on balance and mobility exercises if fitness levels are low"
            ],
            "Mental Wellness": [
                "Engage in relaxation techniques such as deep breathing, guided imagery, or progressive muscle relaxation.",
                "Seek support through counseling or support groups if experiencing anxiety."
            ],
            "Hydration": [
                "Increase water intake to aid in blood pressure management; avoid excessive alcohol and caffeinated beverages.",
                "Monitor sodium levels in hydration drinks, and consider water infused with citrus fruits or cucumber for variety."
            ],
            "Sleep Hygiene": [
                "Prioritize a consistent sleep routine; aim for 7-8 hours of sleep per night.",
                "Reduce caffeine intake, especially in the afternoon, and create a calming bedtime environment."
            ],
            "Additional Health Tips": [
                "Monitor blood pressure regularly at home or with a healthcare provider.",
                "Limit salt intake to 1500 mg per day and choose natural herbs and spices to flavor food.",
                "Manage weight through balanced eating and regular physical activity."
            ]
        }
    }
    return recommendations[risk_level]

# Function to predict and get detailed recommendations
def predict_and_recommend(input_data):
    risk_prediction = model.predict([input_data])[0]  # Predict risk level (0 or 1)
    recommendations = get_detailed_recommendations(risk_prediction)
    return risk_prediction, recommendations

# Example usage of prediction and recommendation
new_data = [26.5, 88, 135, 85, 40]  # Example input: [BMI, heart_rate, systolic_bp, diastolic_bp, age]
risk_level, recommendations = predict_and_recommend(new_data)

print(f"Predicted Hypertension Risk Level: {'High' if risk_level == 1 else 'Low'}\n")
print("Recommendations:")
for category, items in recommendations.items():
    print(f"\n{category}:")
    for item in items:
        print(f"- {item}")
