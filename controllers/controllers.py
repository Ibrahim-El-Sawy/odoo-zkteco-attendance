import json
from odoo import http
from odoo.http import request
from datetime import datetime, timedelta

class DataAPIController(http.Controller):

    @http.route('/data/json', methods=["POST"], type='json', auth='none', csrf=False)
    def data_handle(self, **kwargs):
        raw_data = request.httprequest.data.decode()
        created_ids = []

        def valid(data):
            attendance = {}
            for log in data.get("Logs", []):
                emp = log.get("EmpCode")
                name = log.get("Name")
                mode = log.get("InOutMode", "").lower().strip()
                ts_str = log["Timestamp"]
                ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                date_str = ts.date().isoformat()

                key = (emp, date_str)
                if key not in attendance:
                    attendance[key] = {
                        "name": name,
                        "emp": emp,
                        "check_in": None,
                        "check_out": None,
                        "all_times": []
                    }

                attendance[key]["all_times"].append(ts)
                if "in" in mode:
                    if attendance[key]["check_in"] is None:
                        attendance[key]["check_in"] = ts_str
                    else:
                        attendance[key]["check_out"] = ts_str
                elif "out" in mode:
                    attendance[key]["check_out"] = ts_str

            for key, record in attendance.items():
                if record["check_in"] and not record["check_out"]:
                    sorted_times = record["all_times"]
                    if len(sorted_times) > 1:
                        record["check_out"] = sorted_times[-1].strftime("%Y-%m-%d %H:%M:%S")

                employee = request.env['hr.employee'].sudo().search([
                    ('name', '=', record["name"])
                ], limit=1)

                vals = {
                    "name": employee.id if employee else False,
                    "date_only": datetime.strptime(record["check_in"], "%Y-%m-%d %H:%M:%S").date(),
                    "check_in": datetime.strptime(record["check_in"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=2),
                    "check_out": datetime.strptime(record["check_out"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=2)
                }

                existing = request.env["data.attendance"].sudo().search([
                    ('name', '=', employee.id if employee else False),
                    ('date_only', '=', vals["date_only"])
                ], limit=1)

                if existing:
                    update_vals = {}
                    if not existing.check_in and vals["check_in"]:
                        update_vals["check_in"] = vals["check_in"]
                    if not existing.check_out and vals["check_out"]:
                        update_vals["check_out"] = vals["check_out"]

                    if update_vals:
                        existing.sudo().write(update_vals)
                    rec = existing
                else:
                    rec = request.env["data.attendance"].sudo().create(vals)

                created_ids.append(rec.id)

        try:
            data = json.loads(raw_data)
            valid(data)
            return {
                "Result": "OK",
                "Message": "Logs Saved Successfully",
                "SavedRecords": created_ids,
            }
        except Exception as e:
            return ({"Result": "Error", "Message": f"Invalid JSON: {e}"}, 400)
        finally:
            return('success connection')
