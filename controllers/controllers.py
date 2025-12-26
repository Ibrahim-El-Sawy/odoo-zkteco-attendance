import json
from odoo import http
from odoo.http import request
from datetime import datetime, timedelta
from . import logic_method

class DataAPIController(http.Controller):

    @http.route('/data/json', methods=["POST"], type='json', auth='none', csrf=False)
    def data_handle(self, **kwargs):
        raw_data = request.httprequest.data.decode()
        # created_ids = []
        try:
            data = json.loads(raw_data)
            logic_method.valid(data)
            return {
                "Result": "OK",
                "Message": "Logs Saved Successfully",
                # "SavedRecords": created_ids,
            }
        except Exception as e:
            return ({"Result": "Error", "Message": f"Invalid JSON: {e}"}, 400)
        
