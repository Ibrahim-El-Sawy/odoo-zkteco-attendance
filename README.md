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
