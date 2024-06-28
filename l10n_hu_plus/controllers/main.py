# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, http, models, tools
from odoo.http import request

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusApiController(http.Controller):
    @http.route(
        '/v1/l10n_hu_plus/object',
        auth="public",
        csrf=False,
        methods=["GET"],
        type="json",
        website=False,
    )
    def l10n_hu_plus_v1_object(self):
        # We want to know about every call made to the endpoint, so we just forward
        json_result = request.env['l10n.hu.plus.log'].l10n_hu_plus_api_json_request_response(request)
        # raise exceptions.UserError("json_result" + str(json_result))

        json_response_result = json_result.get('response_result', {})
        # raise exceptions.UserError("json_response_result" + str(json_response_result))

        json_response_values = json_response_result.get('response_values', {})
        # raise exceptions.UserError("json_response_values" + str(json_response_values))

        json_response_data = json_response_values.get('response_data', {})
        # raise exceptions.UserError("json_response_data" + str(json_response_data))

        # Return
        return json_response_data

    @http.route(
        '/v1/l10n_hu_plus/registration',
        auth="public",
        csrf=False,
        methods=["DELETE", "GET", "POST"],
        type="json",
        website=False,
    )
    def l10n_hu_plus_v1_registration(self):
        # We want to know about every call made to the endpoint, so we just forward
        json_result = request.env['l10n.hu.plus.log'].l10n_hu_plus_api_json_request_response(request)
        # raise exceptions.UserError("json_result" + str(json_result))

        json_response_result = json_result.get('response_result', {})
        # raise exceptions.UserError("json_response_result" + str(json_response_result))

        json_response_values = json_response_result.get('response_values', {})
        # raise exceptions.UserError("json_response_values" + str(json_response_values))

        json_response_data = json_response_values.get('response_data', {})
        # raise exceptions.UserError("json_response_data" + str(json_response_data))

        # Return
        return json_response_data
