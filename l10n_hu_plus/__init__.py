def _set_audittrail(env):
    """ 
       Setting audit trail for existing companies.
    """
    env['res.company'].search([]).check_account_audit_trail = True


def _l10nhuplus_post_init(env):
    _set_audittrail(env)

from . import models
from . import wizard
