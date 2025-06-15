
# Network Intrusion Detection System

An ML-based system for detecting network attacks with binary (attack/normal) and multiclass (attack type) classification capabilities.

## 📁 Repository Structure

```
project/
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── samples/
│   ├── attack_sample.json    # Example attack traffic
│   └── normal_sample.json    # Example normal traffic
├── README.md                 # This file
└── .gitignore                # Ignores model files
```

## 🔧 Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Google Drive account (for model download)
- Postman or curl for API testing

### 2. Download Models
Models are too large for GitHub. Download them from:  
🔗 [Google Drive Folder](https://drive.google.com/drive/folders/1deB6nlLj0mgBXC2Xc4_AN20xq3CLlssv?usp=sharing)

```bash
# Create models directory
mkdir -p no_svm_models

# Download all files from Google Drive to this directory
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
Server will start at: `http://localhost:5000`

## 🚀 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict/binary` | POST | Binary classification (Attack/Normal) |
| `/predict/multiclass` | POST | Attack type classification |
| `/analyze` | POST | Detailed traffic analysis |

## 🧪 Testing with Postman

1. **Import the sample JSON files**:
   - Use the `attack_sample.json` and `normal_sample.json` from the `samples/` folder

2. **Test Binary Classification**:
   - **Request**:
     ```
     POST http://localhost:5000/predict/binary
     Headers: Content-Type: application/json
     Body: Select "raw" and paste contents from normal_sample.json
     ```
   - **Expected Normal Response**:
     ```json
     {
         "interpretation": "Normal",
         "probability": 0.23,
         "prediction": 0
     }
     ```

3. **Test Attack Detection**:
   - Use `attack_sample.json` with the same endpoint
   - **Expected Attack Response**:
     ```json
     {
         "interpretation": "Attack",
         "probability": 0.92,
         "prediction": 1
     }
     ```

## 🛠️ Development

### Rebuilding Models
If you need to retrain the models:

```bash
python train.py  # Your training script
```

### Environment Variables
Configure in `app.py`:
```python
ATTACK_THRESHOLD = 0.6  # Sensitivity adjustment
```

## 📊 Model Performance

| Model Type | Accuracy | F1 Score |
|------------|----------|----------|
| Binary | 97.4% | 97.5% |
| Multiclass | 92.6% | 92.1% |

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## 📜 License
MIT © 2023 [Your Name]
```

## Key Features of This README:

1. **Clear Google Drive Integration**:
   - Explicit instructions for model download
   - Visual folder structure showing what's excluded from GitHub

2. **Postman Testing Made Easy**:
   - Ready-to-use sample JSON files
   - Copy-paste request examples
   - Expected responses for verification

3. **Comprehensive Setup**:
   - Step-by-step from environment setup to API testing
   - Includes both CLI and GUI (Postman) methods

4. **Maintenance Info**:
   - Model retraining instructions
   - Configuration options
   - Contribution guidelines

5. **Visual Organization**:
   - Clean markdown formatting
   - Tables for endpoints and performance metrics
   - Clear section headers

This README ensures users can:
1. Quickly set up the project
2. Understand where large files are stored
3. Test the API immediately
4. Know how to modify or extend the system
