import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class HealthAnalysisSystem:
    def __init__(self):
        self.scaler = StandardScaler()
        self.risk_classifier = RandomForestClassifier()
        self.trend_predictor = GradientBoostingRegressor()
        self.pattern_clusterer = KMeans(n_clusters=4)
        
    def preprocess_data(self, data):
        """Preprocess the health data."""
        numerical_cols = ['Weight', 'Height', 'Blood_Pressure_Systolic', 'Heart_Rate', 
                         'Body_Temp', 'BMI', 'Glucose', 'Cholesterol', 'Oxygen']
        data_subset = data[numerical_cols].copy()
        data_scaled = self.scaler.fit_transform(data_subset)
        return pd.DataFrame(data_scaled, columns=numerical_cols)
    
    def assess_health_risks(self, data):
        """Assess various health risks based on vital signs."""
        risks = {}
        
        # Cardiovascular risk assessment
        cv_risk = self._assess_cardiovascular_risk(
            data['Blood_Pressure_Systolic'].iloc[-1], 
            data['Heart_Rate'].iloc[-1],
            data['Cholesterol'].iloc[-1]
        )
        risks['cardiovascular_risk'] = cv_risk
        
        # Diabetes risk assessment
        diabetes_risk = self._assess_diabetes_risk(
            data['Glucose'].iloc[-1],
            data['BMI'].iloc[-1],
            data['Activity_Steps'].iloc[-1]
        )
        risks['diabetes_risk'] = diabetes_risk
        
        # Overall health score
        health_score = self._calculate_health_score(data.iloc[-1])
        risks['health_score'] = health_score
        
        return risks
    
    def _assess_cardiovascular_risk(self, bp, hr, chol):
        """Assess cardiovascular risk based on blood pressure, heart rate, and cholesterol."""
        risk_score = 0
        
        if bp >= 140: risk_score += 2
        elif bp >= 130: risk_score += 1
        
        if hr >= 100: risk_score += 1
        elif hr <= 60: risk_score += 1
        
        if chol >= 240: risk_score += 2
        elif chol >= 200: risk_score += 1
        
        risk_levels = {
            0: 'Low',
            1: 'Moderate-Low',
            2: 'Moderate',
            3: 'Moderate-High',
            4: 'High'
        }
        
        return risk_levels.get(risk_score, 'High')
    
    def _assess_diabetes_risk(self, glucose, bmi, activity):
        """Assess diabetes risk based on glucose, BMI, and activity level."""
        risk_score = 0
        
        if glucose >= 126: risk_score += 2
        elif glucose >= 100: risk_score += 1
        
        if bmi >= 30: risk_score += 2
        elif bmi >= 25: risk_score += 1
        
        if activity <= 5000: risk_score += 1
        
        risk_levels = {
            0: 'Low',
            1: 'Moderate-Low',
            2: 'Moderate',
            3: 'Moderate-High',
            4: 'High'
        }
        
        return risk_levels.get(risk_score, 'High')
    
    def _calculate_health_score(self, data):
        """Calculate overall health score based on all parameters."""
        score = 100
        
        if data['BMI'] > 25: score -= 5
        if data['Blood_Pressure_Systolic'] > 120: score -= 5
        if data['Glucose'] > 100: score -= 5
        if data['Cholesterol'] > 200: score -= 5
        if data['Oxygen'] < 95: score -= 5
        if data['Activity_Steps'] < 5000: score -= 5
        if data['Sleep_Hours'] < 7: score -= 5
        
        return max(0, score)

    def get_recommendations(self, data, risks):
        """Generate personalized recommendations based on health data and risks."""
        recommendations = []
        
        # Cardiovascular recommendations
        if risks['cardiovascular_risk'] in ['Moderate-High', 'High']:
            recommendations.append({
                'category': 'Cardiovascular',
                'recommendation': 'Start with low-impact cardio exercises',
                'details': 'Consider walking, swimming, or cycling for 30 minutes daily'
            })
        
        # Weight management
        if data['BMI'].iloc[-1] >= 25:
            recommendations.append({
                'category': 'Weight Management',
                'recommendation': 'Focus on weight management',
                'details': 'Aim for 150 minutes of moderate exercise per week and maintain a balanced diet'
            })
        
        # Activity level
        if data['Activity_Steps'].iloc[-1] <= 5000:
            recommendations.append({
                'category': 'Physical Activity',
                'recommendation': 'Increase daily activity',
                'details': 'Start with 10-minute walks and gradually increase duration'
            })
        
        # Sleep
        if data['Sleep_Hours'].iloc[-1] < 7:
            recommendations.append({
                'category': 'Sleep',
                'recommendation': 'Improve sleep habits',
                'details': 'Aim for 7-9 hours of sleep per night'
            })
            
        return recommendations
