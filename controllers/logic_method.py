from datetime import datetime, timedelta
from odoo.http import request

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

                employee1 = request.env['hr.employee'].sudo().search([
                    ('barcode', '=', record["emp"])
                ], limit=1)
                print(employee1.name)

                vals = {
                    "name": employee1.id if employee1 else False,
                    "date_only": datetime.strptime(record["check_in"], "%Y-%m-%d %H:%M:%S").date(),
                    "check_in": datetime.strptime(record["check_in"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=2),
                    "check_out": datetime.strptime(record["check_out"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=2)
                }

                existing = request.env["data.attendance"].sudo().search([
                    ('name', '=', employee1.name if employee1 else False),
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

                # created_ids.append(rec.id)