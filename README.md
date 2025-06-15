
# 🛠️ Complete Installation & Testing Guide

## 🌟 **Step 1: System Setup**
### **1.1 Install Python**
```bash
# Windows (PowerShell):
winget install Python.Python.3.10

# macOS/Linux:
brew install python  # or sudo apt-get install python3.8
```

### **1.2 Clone Repository**
```bash
git clone https://github.com/yourusername/network-intrusion-detection.git
cd network-intrusion-detection
```

---

## 📦 **Step 2: Download Model Files**
1. **Access Google Drive**:
   🔗 [Models Folder](https://drive.google.com/drive/folders/1deB6nlLj0mgBXC2Xc4_AN20xq3CLlssv?usp=sharing)

2. **Download Options**:
   - **Option A**: Download all files manually
     - Select all 10 `.pkl` files → Right-click → Download
     - Extract ZIP to `models/` folder

   - **Option B**: Command-line (Linux/macOS):
     ```bash
     mkdir -p models
     gdown --folder 1deB6nlLj0mgBXC2Xc4_AN20xq3CLlssv -O models/
     ```
     *(Requires `pip install gdown`)*

3. **Verify Files**:
   ```bash
   ls -lh models/
   # Should show 10 files, each 150-200MB
   ```

---

## 🐍 **Step 3: Python Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows):
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚦 **Step 4: Run the Server**
```bash
python app1.py
```
**Expected Output**:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```
*(Keep this terminal open)*

---

## 🔍 **Step 5: Test with Postman**
### **5.1 Install Postman**
- Download from [postman.com/downloads](https://www.postman.com/downloads/)
- Install with default settings

### **5.2 Create Requests**
1. **New Collection** → Name it "IDS API Tests"
2. **Add Request** → Name "Check Normal Traffic":
   ```
   POST http://localhost:5000/predict/binary
   Headers:
     Content-Type: application/json
   Body (raw JSON):
   ```
   Paste contents from `no_attack_sample.txt`

3. **Duplicate Request** → Name "Check Attack Traffic":
   Replace body with `attack_sample.txt` content

### **5.3 Sample Test Data**
Create these files in `/samples`:

**no_attack_sample.txt**:
```json
{
    "dur": 0.121478,
    "proto": "tcp",
    "service": "http",
    "state": "FIN",
    "spkts": 6,
    "dpkts": 4,
    "sbytes": 258,
    "dbytes": 172,
    "rate": 74.08749,
    "sttl": 252,
    "dttl": 254,
    "sload": 14158.94238,
    "dload": 8495.365234,
    "sloss": 0,
    "dloss": 0,
    "sinpkt": 24.2956,
    "dinpkt": 8.375,
    "sjit": 30.177547,
    "djit": 11.830604,
    "swin": 255,
    "stcpb": 621772692,
    "dtcpb": 2202533631,
    "dwin": 255,
    "tcprtt": 0.5,
    "synack": 0.3,
    "ackdat": 0.2,
    "smean": 43,
    "dmean": 43,
    "trans_depth": 0,
    "response_body_len": 0,
    "ct_srv_src": 1,
    "ct_state_ttl": 0,
    "ct_dst_ltm": 1,
    "ct_src_dport_ltm": 1,
    "ct_dst_sport_ltm": 1,
    "ct_dst_src_ltm": 1,
    "ct_ftp_cmd": 0,
    "ct_src_ltm": 1,
    "ct_srv_dst": 1
}
```

**attack_sample.txt**:
```json
{
    "dur": 185.2,
    "proto": "udp",
    "service": "unknown",
    "state": "CON",
    "spkts": 15000,
    "dpkts": 3,
    "sbytes": 7500000,
    "dbytes": 120,
    "rate": 99.99,
    "sttl": 55,
    "dttl": 254,
    "sload": 99999.9,
    "dload": 0.5,
    "sloss": 0,
    "dloss": 14997,
    "sinpkt": 0.0001,
    "dinpkt": 0.5,
    "sjit": 0.0,
    "djit": 15.2,
    "swin": 32,
    "stcpb": 0,
    "dtcpb": 0,
    "dwin": 255,
    "tcprtt": 0.0,
    "synack": 0.0,
    "ackdat": 0.0,
    "smean": 8000,
    "dmean": 1,
    "trans_depth": 0,
    "response_body_len": 0,
    "ct_srv_src": 1,
    "ct_state_ttl": 0,
    "ct_dst_ltm": 1,
    "ct_src_dport_ltm": 1,
    "ct_dst_sport_ltm": 0,
    "ct_dst_src_ltm": 0,
    "ct_ftp_cmd": 0,
    "ct_src_ltm": 1,
    "ct_srv_dst": 0
}
```

---

## 🧪 **Step 6: Alternative Testing (CURL)**
### **Test Normal Traffic**
```bash
curl -X POST http://localhost:5000/predict/binary \
  -H "Content-Type: application/json" \
  -d '{
    "dur": 0.12,
    "proto": "tcp",
    "service": "http",
    "state": "FIN",
    "spkts": 6,
    "dpkts": 4
  }'
```

### **Test Attack Traffic**
```bash
curl -X POST http://localhost:5000/predict/binary \
  -H "Content-Type: application/json" \
  -d '{
    "dur": 185.2,
    "proto": "udp",
    "service": "unknown",
    "state": "CON",
    "spkts": 15000,
    "dpkts": 3
  }'
```

---

## 🚨 **Troubleshooting Guide**

| Symptom | Solution |
|---------|----------|
| Model loading errors | Verify all 10 files exist in `models/` |
| Python import errors | Run `pip install -r requirements.txt --force-reinstall` |
| Port 5000 in use | Change port in `app.py`: `app.run(port=5001)` |
| JSON parsing errors | Validate your JSON at [jsonlint.com](https://jsonlint.com/) |
| Slow predictions | Reduce features or upgrade hardware |

---

## 📂 **GitHub Repository Structure**
```
network-intrusion-detection/
├── app.py
├── requirements.txt
├── models/          # .gitignored
│   ├── *.pkl               # 10 model files
├── samples/
│   ├── attack_sample.txt
│   └── no_attack_sample.txt
├── .gitignore              # Ignores model files
└── README.md
```

**`.gitignore` Content**:
```
# Model files
models/*.pkl

# Virtual environment
venv/
```

