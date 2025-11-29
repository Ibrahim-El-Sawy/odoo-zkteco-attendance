{
    'name': "Apis Attendance",
    'summary': "API to receive and process attendance logs from ZKTeco devices",
    'description': """
            This module provides a REST JSON API endpoint for receiving attendance logs
            from ZKTeco biometric devices. It parses check-in/check-out times, prevents 
            duplicates, and stores attendance records in a custom model linked to employees.
    """,

    'website': "https://github.com/ibrahim-elsawy",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

