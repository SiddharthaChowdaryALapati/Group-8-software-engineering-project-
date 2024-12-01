import pandas as pd
from datetime import datetime

def get_bmi_recommendations(bmi):
    """Generate BMI-based recommendations"""
    if bmi < 18.5:
        return {
            "status": "Underweight",
            "recommendations": [
                "Increase caloric intake with nutrient-dense foods",
                "Consider consulting a nutritionist",
                "Add strength training to exercise routine",
                "Track daily calorie intake"
            ]
        }
    elif bmi < 24.9:
        return {
            "status": "Normal weight",
            "recommendations": [
                "Maintain current healthy weight",
                "Regular exercise routine",
                "Balanced diet",
                "Regular health check-ups"
            ]
        }
    elif bmi < 29.9:
        return {
            "status": "Overweight",
            "recommendations": [
                "Gradually increase physical activity",
                "Monitor portion sizes",
                "Focus on whole foods",
                "Consider consulting a healthcare provider"
            ]
        }
    else:
        return {
            "status": "Obese",
            "recommendations": [
                "Consult healthcare provider",
                "Create a sustainable weight loss plan",
                "Regular physical activity",
                "Consider working with a dietitian"
            ]
        }

def get_blood_pressure_recommendations(bp_str):
    """Generate blood pressure recommendations"""
    try:
        systolic, diastolic = map(int, bp_str.split('/'))
        
        if systolic < 120 and diastolic < 80:
            return {
                "status": "Normal",
                "recommendations": [
                    "Maintain healthy lifestyle",
                    "Regular blood pressure monitoring",
                    "Continue balanced diet"
                ]
            }
        elif systolic < 130 and diastolic < 80:
            return {
                "status": "Elevated",
                "recommendations": [
                    "Increase physical activity",
                    "Reduce sodium intake",
                    "Monitor BP more frequently",
                    "Stress management"
                ]
            }
        else:
            return {
                "status": "High",
                "recommendations": [
                    "Consult healthcare provider",
                    "Daily BP monitoring",
                    "Reduce sodium intake",
                    "Regular exercise",
                    "Stress management techniques"
                ]
            }
    except:
        return {
            "status": "Invalid BP reading",
            "recommendations": ["Please provide valid blood pressure reading"]
        }

def get_glucose_recommendations(glucose):
    """Generate glucose-based recommendations"""
    if glucose < 100:
        return {
            "status": "Normal",
            "recommendations": [
                "Maintain healthy diet",
                "Regular exercise",
                "Annual glucose screening"
            ]
        }
    elif glucose < 126:
        return {
            "status": "Prediabetes",
            "recommendations": [
                "Increase physical activity",
                "Monitor carbohydrate intake",
                "Regular glucose testing",
                "Consult healthcare provider"
            ]
        }
    else:
        return {
            "status": "Diabetes range",
            "recommendations": [
                "Immediate healthcare provider consultation",
                "Regular glucose monitoring",
                "Strict dietary management",
                "Regular exercise routine"
            ]
        }

def generate_health_recommendations(health_data):
    """Generate comprehensive health recommendations"""
    recommendations = {
        "bmi_recommendations": get_bmi_recommendations(health_data["bmi"]),
        "blood_pressure_recommendations": get_blood_pressure_recommendations(health_data["blood_pressure"]),
        "glucose_recommendations": get_glucose_recommendations(health_data["glucose"]),
        "general_lifestyle_recommendations": [
            "Aim for 7-9 hours of sleep daily",
            "Stay hydrated with 8 glasses of water",
            "Include 30 minutes of physical activity daily",
            "Eat a balanced diet with plenty of vegetables"
        ],
        "monitoring_recommendations": {
            "daily": [
                "Blood pressure",
                "Physical activity",
                "Water intake"
            ],
            "weekly": [
                "Weight",
                "Exercise log",
                "Sleep pattern"
            ],
            "monthly": [
                "Body measurements",
                "Health goals review"
            ]
        }
    }
    return recommendations