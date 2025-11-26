REST API module for Odoo that receives and processes attendance logs from ZKTeco biometric devices.  
This project provides a JSON endpoint, parses check-in/check-out times, prevents duplicate records,  
and stores attendance data in a custom Odoo model linked to employees.

Features:
- JSON POST endpoint for ZKTeco devices
- Automatic check-in/check-out detection
- Duplicate attendance prevention
- Firmware date parsing
- Custom attendance model
- Integration with hr.employee

Perfect for companies using ZKTeco devices and needing automated attendance synchronization with Odoo.


**Body Example (ZKTeco old Format):**
```json
data = {
    "Result": "OK",
    "DeviceInfo": {
        "DeviceName": "ZKTeco iFace 880",
        "SerialNumber": "SN202512345",
        "FirmwareVersion": "Ver 6.60 Oct 2023",
        "IP": "192.168.1.201"
    },
    "Logs": [
        {
            "UserID": "1",
            "EmpCode": "1201",
            "Name": "Ahmed Ali",
            "VerifyMode": "Finger",
            "InOutMode": "Check-in",
            "Timestamp": "2025-01-22 08:31:12",
            "WorkCode": "0",
            "DeviceID": "1",
            "RawData": "12,Finger,2025-01-22 08:31:12"
        },
        {
            "UserID": "1",
            "EmpCode": "1201",
            "Name": "Ahmed Ali",
            "VerifyMode": "Face",
            "InOutMode": "Check-out",
            "Timestamp": "2025-01-22 17:05:44",
            "WorkCode": "0",
            "DeviceID": "1",
            "RawData": "12,Face,2025-01-22 17:05:44"
        },
        {
            "UserID": "2",
            "EmpCode": "3301",
            "Name": "Mona Adel",
            "VerifyMode": "Card",
            "InOutMode": "Check-in",
            "Timestamp": "2025-01-22 08:55:03",
            "WorkCode": "0",
            "DeviceID": "1",
            "RawData": "33,Card,2025-01-22 08:55:03"
        }
    ]
}

