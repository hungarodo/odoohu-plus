# -*- coding: utf-8 -*-
# 1 : imports of python lib
import re
# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuNavReportWizard(models.TransientModel):
    # Private attributes
    _inherit = 'l10n.hu.wizard'

    # Default methods
    @api.model
    def _get_default_nav_report(self):
        if self._context.get('active_model') and self._context['active_model'] == 'l10n.hu.nav.report':
            nav_report_ids = self._context.get('active_ids', [])
        elif self._context.get('nav_report_ids'):
            nav_report_ids = self._context.get('nav_report_ids', [])
        else:
            nav_report_ids = []
        return [(4, x, 0) for x in nav_report_ids]

    # Field declarations
    # # COMMON
    action_type = fields.Selection(
        ondelete={
            'nav_report': 'cascade',
        },
        selection_add=[
            ('nav_report', "NAV Report"),
        ]
    )
    # # NAV REPORT
    action_nav_report = fields.Selection(
        default='run_report',
        selection=[
            ('run_report', "Run Report"),
            ('print_report', "Print Report")
        ],
        string="NAV Report Action",
    )
    action_nav_report_editable = fields.Boolean(
        default=True,
        string="NAV Report Action Editable",
    )
    action_nav_report_required = fields.Boolean(
        default=False,
        string="NAV Report Action Required",
    )
    action_nav_report_visible = fields.Boolean(
        default=False,
        string="NAV Report Action Visible",
    )
    nav_report = fields.Many2many(
        comodel_name='l10n.hu.nav.report',
        column1='wizard',
        column2='nav_report',
        default=_get_default_nav_report,
        relation='l10n_hu_wizard_nav_report_rel',
        string="NAV Report",
    )
    nav_report_editable = fields.Boolean(
        default=False,
        string="NAV Report Editable",
    )
    nav_report_print_locked = fields.Boolean(
        default=False,
        string="NAV Report Print Locked",
    )
    nav_report_required = fields.Boolean(
        default=False,
        string="NAV Report Required",
    )
    nav_report_visible = fields.Boolean(
        default=False,
        string="NAV Report Visible",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods
    def action_execute(self):
        # Ensure one
        self.ensure_one()

        # Process actions
        # # REPORT
        if self.action_type == 'nav_report':
            # # # run_report
            if self.action_nav_report == 'print_report':
                # Check input
                if not self.nav_report:
                    raise exceptions.UserError(_("NAV Report is mandatory!"))

                # Manage result
                manage_result = self.manage_nav_report()

                # Wizard result
                if manage_result.get('nav_report_ids'):
                    result = {
                        'name': _("NAV Report"),
                        'domain': [('id', 'in', manage_result['nav_report_ids'])],
                        'res_model': 'l10n.hu.nav.report',
                        'target': 'current',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'tree,form',
                    }
                else:
                    raise exceptions.UserError("print_report error!")
            # # # run_report
            elif self.action_nav_report == 'run_report':
                # Check input
                if not self.nav_report:
                    raise exceptions.UserError(_("NAV Report is mandatory!"))

                # Manage result
                manage_result = self.manage_nav_report()

                # Wizard result
                if manage_result.get('nav_report_ids'):
                    result = {
                        'name': _("NAV Report"),
                        'domain': [('id', 'in', manage_result['nav_report_ids'])],
                        'res_model': 'l10n.hu.nav.report',
                        'target': 'current',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'tree,form',
                    }
                else:
                    raise exceptions.UserError("run_report error!")
            # # # else
            else:
                raise exceptions.UserError("invalid nav_report action!")
        # # PARTNER
        elif self.action_type == 'partner':
            # # # list
            if self.action_partner == 'list':
                # Check input
                if not self.partner:
                    raise exceptions.UserError(_("No partner selected!"))

                # Manage result
                manage_result = self.manage_partner()

                # Wizard result
                if manage_result.get('partner_ids'):
                    result = {
                        'name': _("Partner"),
                        'domain': [('id', 'in', manage_result['partner_ids'])],
                        'res_model': 'res.partner',
                        'target': 'current',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'tree,form',
                    }
                else:
                    raise exceptions.UserError("partner_delete error!")
            # # # else
            else:
                raise exceptions.UserError("invalid partner action!")
        # # PRODUCT
        elif self.action_type == 'product':
            # # # list
            if self.action_product == 'list':
                # Check input
                if not self.product:
                    raise exceptions.UserError(_("No product selected!"))

                # Manage result
                manage_result = self.manage_product()

                # Wizard result
                if manage_result.get('product_ids'):
                    result = {
                        'name': _("Product"),
                        'domain': [('id', 'in', manage_result['product_ids'])],
                        'res_model': 'product.product',
                        'target': 'current',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'tree,form',
                    }
                else:
                    raise exceptions.UserError("product_delete error!")
            # # # else
            else:
                raise exceptions.UserError("invalid product action!")
        # # else
        else:
            raise exceptions.UserError(_("Not yet implemented!"))

        # Return result
        return result

    # Business methods
    @api.model
    def manage_nav_report(self):
        """ Manage NAV report

        :return: dictionary
        """
        # Initialize variables
        nav_reports = []
        nav_report_ids = []
        result = {}

        # Process scenarios
        if self.action_type == 'nav_report' \
                and self.action_nav_report == 'print_report':
            for nav_report in self.nav_report:
                nav_reports.append(nav_report)
                nav_report_ids.append(nav_report.id)
                result = nav_report.print_report({
                    'print_locked': self.nav_report_print_locked
                })
            # raise exceptions.UserError(str(result))
        elif self.action_type == 'nav_report' \
                and self.action_nav_report == 'run_report':
            for nav_report in self.nav_report:
                nav_reports.append(nav_report)
                nav_report_ids.append(nav_report.id)
                result = nav_report.run_report({})
            # raise exceptions.UserError(str(result))
        else:
            pass

        # Update result
        result.update({
            'nav_reports': nav_reports,
            'nav_report_ids': nav_report_ids,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result
