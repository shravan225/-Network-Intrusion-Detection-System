# 🚨 Important Model Files Setup

## 📦 Model Files Download

**The trained model files are too large for GitHub** (total ~1.2GB). You **must** download them separately:

🔗 [Google Drive Models Folder](https://drive.google.com/drive/folders/1deB6nlLj0mgBXC2Xc4_AN20xq3CLlssv?usp=sharing)

### Download Instructions:
1. Open the Google Drive link above
2. Select **all files** in the folder
3. Click "Download" (Google will create a ZIP archive)
4. Unzip the files into the `models/` directory in your project

⚠️ **Critical Directory Structure After Download:**
```
your-project-folder/
├── models/
│   ├── balanced_logistic_regression_binary.pkl
│   ├── balanced_random_forest_binary.pkl
│   ├── lightgbm_binary.pkl
│   ├── voting_classifier_binary.pkl
│   ├── xgboost_binary.pkl
│   ├── balanced_logistic_regression_multiclass.pkl
│   ├── balanced_random_forest_multiclass.pkl
│   ├── lightgbm_multiclass.pkl
│   ├── voting_classifier_multiclass.pkl
│   └── xgboost_multiclass.pkl
```

## 🛠️ Common Setup Problems & Solutions

### ❌ Error: "No models loaded" on startup
**Fix these issues:**
1. **Incorrect Download Location**  
   → Ensure all `.pkl` files are in `models/` (not in subfolders)

2. **Missing Files**  
   → Verify you have all 10 model files from Google Drive

3. **Permission Issues**  
   → On Linux/Mac:  
   ```bash
   chmod 644 models/*.pkl
   ```

4. **Corrupted Downloads**  
   → Re-download the files and verify sizes:
   - Binary models: ~150MB each  
   - Multiclass models: ~200MB each

### ❌ Error: "Feature names mismatch"
**Solution:**  
Delete all files in `models/` and:
1. Redownload from Google Drive
2. **Do not modify** the downloaded model files

## 💻 Quick Start Test

After setting up models, verify the system works:

```bash
# 1. Start the server
python app1.py

# 2. In another terminal, test with:
curl -X POST http://localhost:5000/predict/binary \
  -H "Content-Type: application/json" \
  -d '@samples/normal_sample.json'
```

Expected success response:
```json
{
  "interpretation": "Normal",
  "model": "balanced_random_forest",
  "prediction": 0,
  "probability": 0.23
}
```

## 📝 Postman Testing Guide

1. **Import** the sample JSONs:
   - `attack_sample.json` - Example DoS attack
   - `normal_sample.json` - Regular traffic

2. **Collection Setup**:
   ```http
   POST http://localhost:5000/predict/binary
   Headers:
     Content-Type: application/json
   Body: (select raw JSON and paste file contents)
   ```
