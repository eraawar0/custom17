from odoo import http
from odoo.http import request
import json

class CSRFController(http.Controller):
    @http.route('/web/csrf/token', type='json', auth="user")
    def get_csrf_token(self):
        return {
            'token': request.csrf_token()
        }