
import sys
import os
import requests
from datetime import datetime
from zk import ZK, const
from .zk_config import OLD_DEVICES, ODOO_ENDPOINT
from odoo.http import request


class ZKOldService:
    def process_device(self, device):
        ip = OLD_DEVICES["ip"]
        port = OLD_DEVICES.get("port", 4370)
        zk = ZK(ip, port=port, timeout=5)
        try:
            conn = zk.connect()
            conn.disable_device()
            logs = conn.get_attendance()
            for log in logs:
                payload = {
                    "DeviceInfo": {"FirmwareVersion": "01 Jan 2025"},
                    "Logs": [
                        {
                            "EmpCode": str(log.user_id),
                            "Name": f"{log.user_id}",
                            "InOutMode": "IN" if log.status == 0 else "OUT",
                            "Timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        }
                    ]
                }
                request.env['ir.http']._handle_exception(
                    lambda: request.env['ir.http']._json_response(
                        request.dispatch(f"http://localhost:8069{ODOO_ENDPOINT}", params=payload)
                    )
                )
            conn.enable_device()

        except Exception as e:
            print("Error:", e)
