# -*- coding: utf-8 -*-
# 1 : imports of python lib
import json
import logging

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models, SUPERUSER_ID  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations
_logger = logging.getLogger(__name__)


# UPGRADE
def migrate(cr, version):
    # Initialize variables
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Search EDI journals
    try:
        edi_journals = env['account.journal'].search([('type', '=', 'sale'), ('l10n_hu_edi_disabled', '=', False)])
    except:
        edi_journals = env['account.journal'].search([('type', '=', 'sale')])
    _logger.info("POST EDI journal count: %s", len(edi_journals))

    # Set EDI send to manual
    for edi_journal in edi_journals:
        if edi_journal.company_id.account_fiscal_country_id.code == 'HU':
            _logger.info("POST Setting EDI sending to manual for journal: %s", edi_journal.display_name)
            edi_journal.write({'l10n_hu_edi_sending': 'manual'})

    # Log errors
    _logger.info("POST EDI journal update finished")
