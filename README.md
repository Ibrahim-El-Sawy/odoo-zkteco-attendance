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
        {"UserID": "1", "EmpCode": "041642511264", "Name": "Abigail Peterson", "VerifyMode": "Finger", "InOutMode": "Check-in", "Timestamp": "2025-01-22 08:31:12", "WorkCode": "0", "DeviceID": "1", "RawData": "12,Finger,2025-01-22 08:31:12"},
        {"UserID": "1", "EmpCode": "041642511264", "Name": "Abigail Peterson", "VerifyMode": "Face", "InOutMode": "Check-out", "Timestamp": "2025-01-22 17:05:44", "WorkCode": "0", "DeviceID": "1", "RawData": "12,Face,2025-01-22 17:05:44"},
         {"UserID": "1", "EmpCode": "041244121824", "Name": "Doris Cole", "VerifyMode": "Finger", "InOutMode": "Check-in", "Timestamp": "2025-01-22 08:31:12", "WorkCode": "0", "DeviceID": "1", "RawData": "12,Finger,2025-01-22 08:31:12"},
        {"UserID": "1", "EmpCode": "041244121824", "Name": "Doris Cole", "VerifyMode": "Face", "InOutMode": "Check-out", "Timestamp": "2025-01-22 17:05:44", "WorkCode": "0", "DeviceID": "1", "RawData": "12,Face,2025-01-22 17:05:44"}
    ]
}