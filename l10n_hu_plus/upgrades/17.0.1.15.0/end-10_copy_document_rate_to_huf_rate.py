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
    # Copy values to l10n_hu_huf_rate
    cr.execute("""UPDATE account_move SET l10n_hu_huf_rate=l10n_hu_document_rate WHERE l10n_hu_document_rate IS NOT NULL""")
    _logger.info("account_move l10n_hu_document_rate copied to l10n_hu_huf_rate")
