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
    nav_report = fields.Many2many(
        comodel_name='l10n.hu.nav.report',
        column1='wizard',
        column2='nav_report',
        default=_get_default_nav_report,
        relation='l10n_hu_wizard_nav_report_rel',
        string="NAV Report",
    )
    nav_report_action = fields.Selection(
        default='run_report',
        selection=[
            ('create_report', "Create Report"),
            ('run_report', "Run Report"),
            ('print_report', "Print Report"),
            ('run_rule', "Run Rule")
        ],
        string="NAV Report Action",
    )
    nav_report_action_editable = fields.Boolean(
        default=True,
        string="NAV Report Action Editable",
    )
    nav_report_action_required = fields.Boolean(
        default=False,
        string="NAV Report Action Required",
    )
    nav_report_action_visible = fields.Boolean(
        default=False,
        string="NAV Report Action Visible",
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
    nav_report_rule = fields.Many2one(
        comodel_name='l10n.hu.nav.report.rule',
        string="NAV Report Rule",
    )
    nav_report_template = fields.Many2one(
        comodel_name='l10n.hu.nav.report.template',
        string="NAV Report Template",
    )
    nav_report_visible = fields.Boolean(
        default=False,
        string="NAV Report Visible",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods
    # # SUPER
    def action_execute(self):
        """ Super override of original method in l10n_hu_base app"""
        result = super(L10nHuNavReportWizard, self).action_execute()

        # Process actions
        # # REPORT
        if self.action_type == 'nav_report':
            # run_report
            if self.nav_report_action == 'create_report':
                # Check input
                if not self.nav_report_template:
                    raise exceptions.UserError(_("NAV Report template is mandatory!"))

                # Manage result
                manage_result = self.manage_nav_report()

                # Wizard result
                if len(manage_result.get('nav_report_ids', [])) == 1:
                    result = {
                        'name': _("NAV Report"),
                        'res_id': manage_result['nav_report_ids'][0],
                        'res_model': 'l10n.hu.nav.report',
                        'target': 'current',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form,tree',
                    }
                    return result
                elif len(manage_result.get('nav_report_ids', [])) > 1:
                    result = {
                        'name': _("NAV Report"),
                        'domain': [('id', 'in', manage_result['nav_report_ids'])],
                        'res_model': 'l10n.hu.nav.report',
                        'target': 'current',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'tree,form',
                    }
                    return result
                else:
                    raise exceptions.UserError("print_report error!")
            elif self.nav_report_action == 'print_report':
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
                    return result

                else:
                    raise exceptions.UserError("print_report error!")
            # run_report
            elif self.nav_report_action == 'run_report':
                # Check input
                if not self.nav_report:
                    raise exceptions.UserError(_("NAV Report is mandatory!"))

                # Manage result
                manage_result = self.manage_nav_report()

                # Wizard result
                # Wizard result
                if len(manage_result.get('nav_report_ids', [])) == 1:
                    result = {
                        'name': _("NAV Report"),
                        'res_id': manage_result['nav_report_ids'][0],
                        'res_model': 'l10n.hu.nav.report',
                        'target': 'current',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form,tree',
                    }
                    return result
                elif len(manage_result.get('nav_report_ids', [])) > 1:
                    result = {
                        'name': _("NAV Report"),
                        'domain': [('id', 'in', manage_result['nav_report_ids'])],
                        'res_model': 'l10n.hu.nav.report',
                        'target': 'current',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'tree,form',
                    }
                    return result
                else:
                    raise exceptions.UserError("run_report error!")
            # # # else
            else:
                raise exceptions.UserError("invalid nav_report action!")
        # # else
        else:
            pass

        # Return result
        return result

    # Business methods
    @api.model
    def manage_nav_report(self):
        """ Manage NAV report

        :return: dictionary
        """
        # Initialize variables
        error_list = []
        nav_reports = []
        nav_report_ids = []
        result = {}

        # Process scenarios
        if self.action_type == 'nav_report':
            if self.nav_report_action == 'create_report' and self.nav_report_template:
                create_values = {}
                create_result = self.nav_report_template.create_nav_report_from_template(create_values)
                if create_result.get('nav_report'):
                    nav_reports.append(create_result['nav_report'])
                    nav_report_ids.append(create_result['nav_report'].id)
                error_list += create_result.get('error_list', [])
                # raise exceptions.UserError(str(result))
            elif self.nav_report_action == 'print_report':
                for nav_report in self.nav_report:
                    nav_reports.append(nav_report)
                    nav_report_ids.append(nav_report.id)
                    result = nav_report.print_report({
                        'print_locked': self.nav_report_print_locked
                    })
                # raise exceptions.UserError(str(result))
            elif self.nav_report_action == 'run_report':
                for nav_report in self.nav_report:
                    nav_reports.append(nav_report)
                    nav_report_ids.append(nav_report.id)
                    result = nav_report.run_report({})
                # raise exceptions.UserError(str(result))
            else:
                pass
        else:
            pass

        # Update result
        result.update({
            'error_list': error_list,
            'nav_reports': nav_reports,
            'nav_report_ids': nav_report_ids,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result
