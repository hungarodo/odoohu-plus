# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuNavReportTag(models.Model):
    # Private attributes
    _inherit = 'l10n.hu.tag'

    # Default methods

    # Field declarations
    tag_type = fields.Selection(
        ondelete={
            'nav_report_category': 'cascade',
            'nav_report_tag': 'cascade',
            'nav_report_data_category': 'cascade',
            'nav_report_data_tag': 'cascade',
        },
        selection_add=[
            ('nav_report_category', "NAV Report Category"),
            ('nav_report_tag', "NAV Report Tag"),
            ('nav_report_data_category', "NAV Report Data Category"),
            ('nav_report_data_tag', "NAV Report Data Tag"),
        ]
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
