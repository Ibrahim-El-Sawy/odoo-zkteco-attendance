# ZKTeco → Odoo Attendance Sync  

A complete solution for receiving attendance logs from **ZKTeco devices**, processing them, and sending them into **Odoo ERP** using a custom JSON endpoint.

Perfect for companies using ZKTeco devices and needing automated attendance synchronization with Odoo.

## 📌 Overview
This project contains two main components:

### **1. Python Service**
- Connects to multiple ZKTeco biometric devices  
- Pulls attendance logs  
- Sends each log as JSON to an Odoo endpoint (`/data/json`)

### **2. Odoo JSON API Controller**
- Receives attendance logs  
- Processes IN/OUT  
- Matches employees  
- Creates attendance records inside Odoo  

## Body Example (ZKTeco old Format)
```json
data = {
    "Result": "OK",
    "DeviceInfo": {"DeviceName": "ZKTeco iFace 880", "SerialNumber": "SN202512345", "FirmwareVersion": "Ver 6.60 Oct 2023", "IP": "192.168.1.201"},
    "Logs": [
        {"UserID": "1", "EmpCode": "1201", "Name": "Ahmed Ali", "VerifyMode": "Finger", "InOutMode": "Check-in", "Timestamp": "2025-01-22 08:31:12", "WorkCode": "0", "DeviceID": "1", "RawData": "12,Finger,2025-01-22 08:31:12"},
        {"UserID": "1", "EmpCode": "1201", "Name": "Ahmed Ali", "VerifyMode": "Face", "InOutMode": "Check-out", "Timestamp": "2025-01-22 17:05:44", "WorkCode": "0", "DeviceID": "1", "RawData": "12,Face,2025-01-22 17:05:44"},
        {"UserID": "2", "EmpCode": "3301", "Name": "Mona Adel", "VerifyMode": "Card", "InOutMode": "Check-in", "Timestamp": "2025-01-22 08:55:03", "WorkCode": "0", "DeviceID": "1", "RawData": "33,Card,2025-01-22 08:55:03"}
    ]
}
