import json
from odoo import http
from odoo.http import request
from datetime import datetime

class DataAPIController(http.Controller):

    @http.route('/data/json', methods=["POST"], type='json', auth='none', csrf=False)
    def data_handle(self, **kwargs):
        raw_data = request.httprequest.data.decode()
        try:
            data = json.loads(raw_data)
        except Exception as e:
            return {"Result": "Error", "Message": f"Invalid JSON: {e}"}

        logs = data.get("Logs", [])
        created_ids = []

        def datehandle(text):
            parts = text.split()
            day_str = "01"
            month_str = parts[2]
            year_str = parts[3]
            date_obj = datetime.strptime(f"{day_str} {month_str} {year_str}", "%d %b %Y")
            return date_obj.date()

        jsonDate = datehandle(data["DeviceInfo"]["FirmwareVersion"])

        def valid(data):
            attendance = {}
            logs = data["Logs"]
            for log in logs:
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
                    sorted_times = sorted(record["all_times"])
                    if len(sorted_times) > 1:
                        record["check_out"] = sorted_times[-1].strftime("%Y-%m-%d %H:%M:%S")

                employee = request.env['hr.employee'].sudo().search([
                    ('name', '=', record["name"])
                ], limit=1)

                vals = {
                    "name": employee.id if employee else False,
                    "date_only": datetime.strptime(record["check_in"], "%Y-%m-%d %H:%M:%S").date(),
                    "check_in": record["check_in"],
                    "check_out": record["check_out"],
                }

                rec = request.env["data.attendance"].sudo().create(vals)
                created_ids.append(rec.id)

        valid(data)

        return {
            "Result": "OK",
            "Message": "Logs Saved Successfully",
            "SavedRecords": created_ids,
        }
