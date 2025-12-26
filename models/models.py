from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DataAttendance(models.Model):
    _name = 'data.attendance'
    _description = "Employee Attendance"

    name = fields.Many2one('hr.employee', string="Employee", required=True)
    date_only = fields.Date(string="Date")
    check_in = fields.Datetime(string='Check-in')
    check_out = fields.Datetime(string='Check-out')
    total_hours = fields.Char(string="Total Hours", compute='_compute_total_hours', store=True)

    @api.depends('check_in', 'check_out')
    def _compute_total_hours(self):
        """Compute difference between check_out and check_in in HH:MM format"""
        for record in self:
            if record.check_in and record.check_out:
                delta = record.check_out - record.check_in
                hours, remainder = divmod(delta.total_seconds(), 3600)
                minutes = remainder // 60
                record.total_hours = f"{int(hours):02d}:{int(minutes):02d}"
            else:
                record.total_hours = "00:00"
    @api.model
    def create_or_update(self, vals):
        """Create or update attendance record"""
        date_ref = (vals.get('check_in') or vals.get('check_out')).date()
        record = self.search([
            ('name', '=', vals.get('name')),
            ('date_only', '=', date_ref),
        ], limit=1)

        if record:
            record.write({
                'check_in': vals.get('check_in') or record.check_in,
                'check_out': vals.get('check_out') or record.check_out,
            })
            return record
        else:
            vals['date_only'] = date_ref
            return super().create(vals)

    @api.constrains('name', 'check_in')
    def _check_duplicate_attendance(self):
        """Prevent duplicate attendance for the same employee on the same day"""
        for record in self:
            if record.name and record.check_in:
                start_day = record.check_in.replace(hour=0, minute=0, second=0, microsecond=0)
                end_day = record.check_in.replace(hour=23, minute=59, second=59, microsecond=999999)

                duplicate = self.search([
                    ('name', '=', record.name.id),
                    ('check_in', '>=', start_day),
                    ('check_in', '<=', end_day),
                    ('id', '!=', record.id),
                ], limit=1)

                if duplicate:
                    raise ValidationError(_("This employee already has attendance recorded for the same day."))
