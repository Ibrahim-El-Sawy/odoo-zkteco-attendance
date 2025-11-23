from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DataAttendance(models.Model):
    _name = 'data.attendance'

    name = fields.Many2one('hr.employee', string="Employee")
    date_only = fields.Date(string="Date")
    check_in = fields.Datetime(string='Check-in')
    check_out = fields.Datetime(string='Check-out')

    @api.model
    def create_or_update(self, vals):
        record = self.search([
            ('name', '=', vals.get('name')),
            ('date_only', '=', vals.get('check_in').date() if vals.get('check_in') else vals.get('check_out').date())
        ], limit=1)
        if record:
            record.write({
                'check_in': vals.get('check_in') or record.check_in,
                'check_out': vals.get('check_out') or record.check_out,
            })
            return record
        else:
            vals['date_only'] = (vals.get('check_in') or vals.get('check_out')).date()
            return super().create(vals)
        
    @api.constrains('name', 'check_in')
    def _check_duplicate_attendance(self):
        for record in self:
            if record.name and record.check_in:
                start_day = record.check_in.replace(hour=0, minute=0, second=0)
                end_day = record.check_in.replace(hour=23, minute=59, second=59)

                domain = [
                    ('name', '=', record.name.id),
                    ('check_in', '>=', start_day),
                    ('check_in', '<=', end_day),
                    ('id', '!=', record.id),
                ]

                duplicate = self.search(domain, limit=1)
                if duplicate:
                    raise ValidationError("This employee already has attendance recorded for the same day.")

class Data(models.Model):
    _name = 'data'

    UserID = fields.Integer(exportable=True)
    EmpCode = fields.Integer()
    Name = fields.Char(exportable=True)
    VerifyMode = fields.Selection([
        ("finger", "Finger"),
        ("face", "Face"),
        ("card", "Card")
    ], exportable=True)

    InOutMode = fields.Selection([
        ("check-in", "Check-in"),
        ("check-out", "Check-out")
    ], exportable=True)

    Timestamp = fields.Datetime(exportable=True)

    def _export_rows(self, fields_to_export):
        rows = []

        for rec in self:
            employee = rec.Name or ""
            check_in = ""
            check_out = ""

            if rec.InOutMode == "check-in":
                check_in = rec.Timestamp
            elif rec.InOutMode == "check-out":
                check_out = rec.Timestamp

            rows.append([
                employee,
                check_in,
                check_out
            ])

        return rows

    def _export_field_name(self, field):
        return {
            "Name": "Employee",
            "check_in": "Check In",
            "check_out": "Check Out",
        }.get(field.name, field.string)
