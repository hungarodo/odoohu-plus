# -*- coding: utf-8 -*-
# 1 : imports of python lib
import logging

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models, SUPERUSER_ID  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations
_logger = logging.getLogger(__name__)


# UPGRADE
def migrate(cr, version):
    # Manage document type model change
    cr.execute("ALTER TABLE account_move ADD COLUMN l10n_hu_document_type_temp int")
    cr.execute("""UPDATE account_move SET l10n_hu_document_type_temp=l10n_hu_document_type WHERE l10n_hu_document_type IS NOT NULL""")
    cr.execute("""UPDATE account_move SET l10n_hu_document_type=NULL""")
