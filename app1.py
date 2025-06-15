from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os
from sklearn.utils.class_weight import compute_class_weight
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)
MODELS_DIR = "models"
ALLOWED_EXTENSIONS = {'csv', 'json'}
ATTACK_THRESHOLD = 0.6  # Adjusted to better catch attacks

models = {
    'binary': {},
    'multiclass': {
        'label_encoder': None
    }
}

ATTACK_RULES = {
    'min_packets': 1000,
    'min_bytes': 1000000,
    'max_duration': 60,
    'suspicious_services': ['unknown', 'snmp', 'icmp']
}

def load_models():
    """Load all trained models from disk"""
    try:
        for model_file in os.listdir(MODELS_DIR):
            if model_file.endswith('_binary.pkl'):
                model_name = model_file.replace('_binary.pkl', '')
                with open(os.path.join(MODELS_DIR, model_file), 'rb') as f:
                    models['binary'][model_name] = pickle.load(f)
        
        for model_file in os.listdir(MODELS_DIR):
            if model_file.endswith('_multiclass.pkl'):
                model_name = model_file.replace('_multiclass.pkl', '')
                with open(os.path.join(MODELS_DIR, model_file), 'rb') as f:
                    models['multiclass'][model_name], models['multiclass']['label_encoder'] = pickle.load(f)
        
        print("All models loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return False

def preprocess_input(input_data):
    """Preprocess input data to match training format"""
    try:
        if not isinstance(input_data, pd.DataFrame):
            input_data = pd.DataFrame([input_data])
        
        input_data['service'] = input_data['service'].replace('-', 'unknown')
        
        input_data['packet_ratio'] = input_data['spkts'] / (input_data['dpkts'] + 1e-6)
        input_data['byte_ratio'] = input_data['sbytes'] / (input_data['dbytes'] + 1e-6)
        input_data['duration_per_packet'] = input_data['dur'] / (input_data['spkts'] + input_data['dpkts'] + 1e-6)
        input_data['response_ratio'] = input_data['response_body_len'] / (input_data['sbytes'] + 1e-6)
        
        cat_cols = ['proto', 'service', 'state']
        input_data = pd.get_dummies(input_data, columns=cat_cols)
        
        model_features = models['binary']['balanced_random_forest'].feature_names_in_
        
        for col in model_features:
            if col not in input_data.columns:
                input_data[col] = 0
        
        input_data = input_data[model_features]
        
        return input_data
        
    except Exception as e:
        raise ValueError(f"Preprocessing failed: {str(e)}")

def detect_suspicious_features(processed_data):
    """Apply rule-based attack detection"""
    suspicious_features = []
    
    if processed_data['spkts'].values[0] > ATTACK_RULES['min_packets']:
        suspicious_features.append("high_packet_count")
    if processed_data['sbytes'].values[0] > ATTACK_RULES['min_bytes']:
        suspicious_features.append("high_byte_volume")
    if processed_data['dur'].values[0] > ATTACK_RULES['max_duration']:
        suspicious_features.append("long_duration")
    
    for service in ATTACK_RULES['suspicious_services']:
        if f"service_{service}" in processed_data.columns:
            if processed_data[f"service_{service}"].values[0] == 1:
                suspicious_features.append(f"suspicious_service_{service}")
                break
    
    return suspicious_features

@app.route('/predict/binary', methods=['POST'])
def predict_binary():
    """Enhanced binary classification endpoint"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
            
        data = request.get_json()
        processed_data = preprocess_input(data)
        
        model = models['binary']['balanced_random_forest']
        proba = model.predict_proba(processed_data)[0][1]
        
        suspicious_features = detect_suspicious_features(processed_data)
        
        if len(suspicious_features) >= 2:
            prediction = 1
            confidence = max(proba, 0.8)  
            decision_source = "rule_based"
        else:
            prediction = 1 if proba >= ATTACK_THRESHOLD else 0
            confidence = proba
            decision_source = "model_based"
        
        return jsonify({
            "prediction": prediction,
            "probability": float(confidence),
            "threshold_used": ATTACK_THRESHOLD,
            "interpretation": "Attack" if prediction == 1 else "Normal",
            "suspicious_features": suspicious_features,
            "decision_source": decision_source,
            "model_used": "balanced_random_forest"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/multiclass', methods=['POST'])
def predict_multiclass():
    """Multiclass classification endpoint"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
            
        data = request.get_json()
        processed_data = preprocess_input(data)
        
        model = models['multiclass']['balanced_random_forest']
        le = models['multiclass']['label_encoder']
        
        proba = model.predict_proba(processed_data)[0]
        pred_class = np.argmax(proba)
        
        if pred_class >= len(le.classes_):
            pred_class = len(le.classes_) - 1
        
        attack_type = le.inverse_transform([pred_class])[0]
        
        return jsonify({
            "prediction": int(pred_class),
            "attack_type": attack_type,
            "probabilities": {
                cls: float(prob) for cls, prob in zip(le.classes_, proba)
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_traffic():
    """Detailed traffic analysis endpoint"""
    try:
        data = request.get_json()
        processed = preprocess_input(data)
        
        analysis = {
            "feature_analysis": {
                "packet_imbalance": float(processed['spkts'].values[0] / (processed['dpkts'].values[0] + 1e-6)),
                "byte_imbalance": float(processed['sbytes'].values[0] / (processed['dbytes'].values[0] + 1e-6)),
                "duration": float(processed['dur'].values[0]),
                "is_suspicious_service": any(
                    f"service_{s}" in processed.columns and processed[f"service_{s}"].values[0] == 1 
                    for s in ATTACK_RULES['suspicious_services']
                )
            },
            "model_predictions": {
                "binary": float(models['binary']['balanced_random_forest'].predict_proba(processed)[0][1]),
                "multiclass": dict(zip(
                    models['multiclass']['label_encoder'].classes_,
                    [float(p) for p in models['multiclass']['balanced_random_forest'].predict_proba(processed)[0]]
                ))
            }
        }
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if not load_models():
    print("Failed to load models. Exiting...")
    exit(1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)