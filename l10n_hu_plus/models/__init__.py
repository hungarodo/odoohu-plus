# -*- coding: utf-8 -*-
def _l10n_hu_plus_set_audit_trail(env):
    """ Setting audit trail for existing companies """
    env['res.company'].search([('account_fiscal_country_id.code', '=', 'HU')]).check_account_audit_trail = True

def _l10n_hu_plus_post_init(env):
    _l10n_hu_plus_set_audit_trail(env)

from . import account_fiscal_position
from . import account_journal
from . import account_move
from . import account_move_line
from . import account_payment_term
from . import account_tag
from . import account_tax
from . import ir_attachment
from . import log
from . import object
from . import res_company
from . import res_partner
from . import tag
from . import uom_uom
