# -*- coding: utf-8 -*-
# 1 : imports of python lib
import base64
import datetime
import lxml

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.tools.misc import formatLang, format_date
from odoo.tools.safe_eval import safe_eval

# 4 : variable declarations


# Class
class L10nHuNavReport(models.Model):
    # Private attributes
    _name = 'l10n.hu.nav.report'
    _description = "HU NAV Report"
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    # Default methods

    # Field declarations
    active = fields.Boolean(
        default=True,
        string="Active",
    )
    category = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'nav_report_category')],
        index=True,
        string="Category",
    )
    category_technical_name = fields.Char(
        related='category.technical_name',
        string="Category Technical Name",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        index=True,
        string="Company",
    )
    description = fields.Text(
        index=True,
        string="Description",
        translate=True,
    )
    input = fields.One2many(
        comodel_name='l10n.hu.nav.report.input',
        inverse_name='report',
        string="Input",
    )
    input_count = fields.Integer(
        compute='_compute_input_count',
        string="Input Count",
    )
    name = fields.Char(
        copy=False,
        string="Name",
    )
    output = fields.One2many(
        comodel_name='l10n.hu.nav.report.output',
        inverse_name='report',
        string="Output",
    )
    output_count = fields.Integer(
        compute='_compute_output_count',
        string="Output Count",
    )
    period_start = fields.Date(
        copy=False,
        string="Period Start",
    )
    period_end = fields.Date(
        copy=False,
        string="Period End",
    )
    status = fields.Selection(
        copy=False,
        default='draft',
        selection=[
            ('draft', "Draft"),
            ('open', "Open"),
            ('done', "Done")
        ],
        string="Status",
    )
    tag = fields.Many2many(
        comodel_name='l10n.hu.tag',
        column1='object',
        column2='tag',
        domain=[('tag_type', 'in', ['general', 'nav_report_tag'])],
        index=True,
        relation='l10n_hu_nav_report_tag_rel',
        string="Tag",
    )
    template = fields.Many2one(
        comodel_name='l10n.hu.nav.report.template',
        index=True,
        required=True,
        string="Template",
    )
    template_code = fields.Char(
        copy=False,
        string="Template Code",
    )
    template_version = fields.Char(
        copy=False,
        string="Template Version",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_input_count(self):
        for record in self:
            record.input_count = self.env['l10n.hu.nav.report.input'].search_count([
                ('report', '=', record.id),
            ])

    def _compute_output_count(self):
        for record in self:
            record.output_count = self.env['l10n.hu.nav.report.output'].search_count([
                ('report', '=', record.id),
            ])

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def write(self, values):
        # Initialize
        record_ids = []
        for record in self:
            record_ids.append(record.id)

        # Do write
        is_updated = super(L10nHuNavReport, self).write(values)

        # Now recompute totals
        updated_records = self.env['l10n.hu.nav.report'].search([
            ('id', 'in', record_ids)
        ])

        # Manage indicators
        for updated_record in updated_records:
            # updated_record.manage_indicators()
            pass

        # return
        return is_updated

    def name_get(self):
        # Initialize variables
        result = []

        # Iterate through self
        for record in self:
            # Set name
            name = "[NAV-REP-" + str(record.id) + "]"

            if record.name:
                name += " " + record.name

            # Append to list
            result.append((record.id, name))

        # Return result
        return result

    # Action methods
    def action_list_inputs(self):
        """ List related inputs """
        # Ensure one
        self.ensure_one()

        # Assemble result
        result = {
            'name': _("Inputs"),
            'domain': [('report', '=', self.id)],
            'res_model': 'l10n.hu.nav.report.input',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    def action_list_outputs(self):
        """ List related outputs """
        # Ensure one
        self.ensure_one()

        # List view
        list_view = self.env.ref('l10n_hu_nav_report.nav_report_output_view_list_report')

        # Assemble result
        result = {
            'name': _("Outputs"),
            'domain': [('report', '=', self.id)],
            'res_model': 'l10n.hu.nav.report.output',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'views': [(list_view.id, 'tree'), (False, 'form')],
        }

        # Return result
        return result

    def action_wizard_print_report(self):
        """ Start wizard to print a report """
        # Ensure one record in self
        self.ensure_one()

        # Assemble context
        context = {
            'default_action_type': 'nav_report',
            'default_action_type_editable': False,
            'default_action_type_visible': False,
            'default_nav_report_action': 'print_report',
            'default_nav_report_action_editable': False,
            'default_nav_report_action_required': True,
            'default_nav_report_action_visible': True,
            'default_nav_report_editable': False,
            'default_nav_report_visible': True,
        }

        # Assemble result
        result = {
            'name': _("HU Wizard"),
            'context': context,
            'res_model': 'l10n.hu.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }

        # Return result
        return result

    def action_wizard_run_report(self):
        """ Start wizard to run a report """
        # Ensure one record in self
        self.ensure_one()

        # Assemble context
        context = {
            'default_action_type': 'nav_report',
            'default_action_type_editable': False,
            'default_action_type_visible': False,
            'default_nav_report_action': 'run_report',
            'default_nav_report_action_editable': False,
            'default_nav_report_action_required': True,
            'default_nav_report_action_visible': True,
            'default_nav_report_editable': False,
            'default_nav_report_visible': True,
        }

        # Assemble result
        result = {
            'name': _("HU Wizard"),
            'context': context,
            'res_model': 'l10n.hu.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }

        # Return result
        return result

    # Business methods
    @api.model
    def print_report(self, values):
        """ Run report dispatch hub """
        result = {}

        # Dispatch
        if self.template and self.template_code in ['2365', '2465']:
            values.update({
                'template_code': self.template_code,
                'template_version': self.template_version,
            })
            result = self.print_report_xml_xx65(values)

        # Return
        return result

    @api.model
    def print_report_xml_xx65(self, values):
        """ Print 65A 65M report as xml """
        # raise exceptions.UserError("print_report_xml_xx65 BEGIN" + str(values))
        # Initialize variables
        result = {}

        # Inspect values
        template_code = values.get('template_code', "")
        template_version = values.get('template_version', "")

        if values.get('print_locked') is not None:
            print_locked = values['print_locked']
        else:
            print_locked = False

        # nyomtatvanyok element
        xmlns_namespace = {
            None: "http://www.apeh.hu/abev/nyomtatvanyok/2005/01"
        }
        nyomtatvanyok_xml = lxml.etree.Element('nyomtatvanyok', nsmap=xmlns_namespace)

        # nyomtatvany_xml
        nyomtatvany_xml = lxml.etree.Element('nyomtatvany')

        # nyomtatvanyinformacio_xml
        nyomtatvanyinformacio_xml = lxml.etree.Element('nyomtatvanyinformacio')

        # nyomtatvanyazonosito_xml
        nyomtatvanyazonosito_xml = lxml.etree.Element('nyomtatvanyazonosito')
        nyomtatvanyazonosito_xml.text = str(template_code) + "A"
        nyomtatvanyinformacio_xml.append(nyomtatvanyazonosito_xml)

        # nyomtatvanyverzio_xml
        nyomtatvanyverzio_xml = lxml.etree.Element('nyomtatvanyverzio')
        nyomtatvanyverzio_xml.text = str(template_version)
        nyomtatvanyinformacio_xml.append(nyomtatvanyverzio_xml)

        # adozo_xml
        adozo_xml = lxml.etree.Element('adozo')

        # adozo_nev_xml
        adozo_nev_xml = lxml.etree.Element('nev')
        adozo_nev_xml.text = str(self.company.partner_id.name)
        adozo_xml.append(adozo_nev_xml)

        # adozo_adoszam_xml
        adozo_adoszam_xml = lxml.etree.Element('adoszam')
        adozo_adoszam_raw = str(self.company.partner_id.l10n_hu_vat)
        adozo_adoszam_xml.text = adozo_adoszam_raw.replace("-", "")
        adozo_xml.append(adozo_adoszam_xml)

        nyomtatvanyinformacio_xml.append(adozo_xml)
        nyomtatvany_xml.append(nyomtatvanyinformacio_xml)

        # mezok_xml
        mezok_xml = lxml.etree.Element('mezok')

        # process outputs
        for output in self.output:
            if print_locked and output.locked:
                processable = True
            elif not print_locked:
                processable = True
            else:
                processable = False

            if processable:
                # mezo
                mezo_xml = lxml.etree.Element('mezo')
                mezo_xml.attrib['eazon'] = output.technical_name
                output_result = output.get_nav_report_output_value({})
                output_value = output_result.get('value_formatted', False)
                mezo_xml.text = str(output_value)
                mezok_xml.append(mezo_xml)

        # Append mezok to nyomtatvany
        nyomtatvany_xml.append(mezok_xml)

        # Append nyomtatvany to nyomtatvanyok
        nyomtatvanyok_xml.append(nyomtatvany_xml)

        # TODO: REFACTOR THIS! HARDCODED!!
        # BEGIN 2365M (one nyomtatvany element per partner, ONLY INCOMING INVOICES!)
        # collect relevant_invoices
        relevant_invoices = self.env['account.move'].sudo().search([
            ('move_type', 'in', ['in_invoice', 'in_refund']),
            ('l10n_hu_vat_date', '>=', self.period_start),
            ('l10n_hu_vat_date', '<=', self.period_end),
            ('partner_id.commercial_partner_id.l10n_hu_vat', '!=', False),
        ])

        # collect relevant_partners
        relevant_partners = []
        for relevant_invoice in relevant_invoices:
            if relevant_invoice.partner_id not in relevant_partners:
                relevant_partners.append(relevant_invoice.partner_id)

        # process partners
        for relevant_partner in relevant_partners:
            partner_invoices = self.env['account.move'].sudo().search([
                ('move_type', 'in', ['in_invoice', 'in_refund']),
                ('l10n_hu_vat_date', '>=', self.period_start),
                ('l10n_hu_vat_date', '<=', self.period_end),
                ('partner_id', '=', relevant_partner.id),
            ])

            # nyomtatvany_xml
            nyomtatvany_xml = lxml.etree.Element('nyomtatvany')

            # BEGIN NYOMTATVANYINFORMACIO
            # nyomtatvanyinformacio_xml
            nyomtatvanyinformacio_xml = lxml.etree.Element('nyomtatvanyinformacio')

            # nyomtatvanyazonosito_xml
            nyomtatvanyazonosito_xml = lxml.etree.Element('nyomtatvanyazonosito')
            nyomtatvanyazonosito_xml.text = str(template_code) + "M"
            nyomtatvanyinformacio_xml.append(nyomtatvanyazonosito_xml)

            # nyomtatvanyverzio_xml
            nyomtatvanyverzio_xml = lxml.etree.Element('nyomtatvanyverzio')
            nyomtatvanyverzio_xml.text = str(template_version)
            nyomtatvanyinformacio_xml.append(nyomtatvanyverzio_xml)

            # BEGIN ADOZO
            # adozo_xml
            adozo_xml = lxml.etree.Element('adozo')

            # adozo_nev_xml
            adozo_nev_xml = lxml.etree.Element('nev')
            adozo_nev_xml.text = str(self.company.partner_id.name)
            adozo_xml.append(adozo_nev_xml)

            # adozo_adoszam_xml
            adozo_adoszam_xml = lxml.etree.Element('adoszam')
            adozo_adoszam_raw = str(self.company.partner_id.l10n_hu_vat)
            adozo_adoszam_xml.text = adozo_adoszam_raw.replace("-", "")
            adozo_xml.append(adozo_adoszam_xml)

            nyomtatvanyinformacio_xml.append(adozo_xml)
            # END ADOZO

            # BEGIN ALBIZONYLATAZONOSITAS (PARTNER!)
            albizonylatazonositas_xml = lxml.etree.Element('albizonylatazonositas')
            
            # albizonylatazonositas_megnevezes_xml
            albizonylatazonositas_megnevezes_xml = lxml.etree.Element('megnevezes')
            albizonylatazonositas_megnevezes_xml.text = str(relevant_partner.name)
            albizonylatazonositas_xml.append(albizonylatazonositas_megnevezes_xml)            
            
            # albizonylatazonositas_azonosito_xml
            albizonylatazonositas_azonosito_xml = lxml.etree.Element('azonosito')
            albizonylatazonositas_azonosito_xml.text = str(relevant_partner.l10n_hu_vat[:8])
            albizonylatazonositas_xml.append(albizonylatazonositas_azonosito_xml)
            
            nyomtatvanyinformacio_xml.append(albizonylatazonositas_xml)
            # END ALBIZONYLATAZONOSITAS
            
            # BEGIN IDOSZAK
            idoszak_xml = lxml.etree.Element('idoszak')
            
            # idoszak_tol_xml
            idoszak_tol_xml = lxml.etree.Element('tol')
            idoszak_tol_xml.text = str(self.period_start).replace("-", "")
            idoszak_xml.append(idoszak_tol_xml)
            
            # idoszak_ig_xml
            idoszak_ig_xml = lxml.etree.Element('ig')
            idoszak_ig_xml.text = str(self.period_end).replace("-", "")
            idoszak_xml.append(idoszak_ig_xml)
            
            nyomtatvanyinformacio_xml.append(idoszak_xml)
            # END ALBIZONYLATAZONOSITAS

            # END NYOMTATVANYINFORMACIO
            nyomtatvany_xml.append(nyomtatvanyinformacio_xml)

            # BEGIN MEZOK
            # mezok_xml
            mezok_xml = lxml.etree.Element('mezok')

            # LAP: 2365M
            # company_vat 0A0001C001A
            mezo_company_vat_xml = lxml.etree.Element('mezo')
            mezo_company_vat_xml.attrib['eazon'] = '0A0001C001A'
            mezo_company_vat_xml.text = str(self.company.partner_id.l10n_hu_vat).replace("-", "")
            mezok_xml.append(mezo_company_vat_xml)

            # company_name 0A0001C004A
            mezo_company_name_xml = lxml.etree.Element('mezo')
            mezo_company_name_xml.attrib['eazon'] = '0A0001C004A'
            mezo_company_name_xml.text = str(self.company.partner_id.name)
            mezok_xml.append(mezo_company_name_xml)

            # partner_vat 0A0001C005A
            mezo_partner_vat_xml = lxml.etree.Element('mezo')
            mezo_partner_vat_xml.attrib['eazon'] = '0A0001C005A'
            mezo_partner_vat_xml.text = str(relevant_partner.l10n_hu_vat)[:8]
            mezok_xml.append(mezo_partner_vat_xml)

            # partner_name 0A0001C006A
            mezo_partner_name_xml = lxml.etree.Element('mezo')
            mezo_partner_name_xml.attrib['eazon'] = '0A0001C006A'
            mezo_partner_name_xml.text = str(relevant_partner.name)
            mezok_xml.append(mezo_partner_name_xml)

            # date_from 0A0001D001A
            mezo_partner_date_from_xml = lxml.etree.Element('mezo')
            mezo_partner_date_from_xml.attrib['eazon'] = '0A0001D001A'
            mezo_partner_date_from_xml.text = str(self.period_start).replace("-", "")
            mezok_xml.append(mezo_partner_date_from_xml)

            # date_to 0A0001D002A
            mezo_partner_date_to_xml = lxml.etree.Element('mezo')
            mezo_partner_date_to_xml.attrib['eazon'] = '0A0001D002A'
            mezo_partner_date_to_xml.text = str(self.period_end).replace("-", "")
            mezok_xml.append(mezo_partner_date_to_xml)

            # LAP: 02 (invoice list)
            invoice_index = 0
            for partner_invoice in partner_invoices:
                # increase index
                invoice_index += 1
                # mezo_invoice_number_xml 0B0001C0001AA
                mezo_invoice_number_xml = lxml.etree.Element('mezo')
                mezo_invoice_number_xml_eazon = '0B0001C000' + str(invoice_index) + 'AA'
                mezo_invoice_number_xml.attrib['eazon'] = mezo_invoice_number_xml_eazon
                mezo_invoice_number_xml.text = str(partner_invoice.ref)
                mezok_xml.append(mezo_invoice_number_xml)

                # mezo_delivery_date_xml 0B0001C0001BA
                mezo_delivery_date_xml = lxml.etree.Element('mezo')
                mezo_delivery_date_xml_eazon = '0B0001C000' + str(invoice_index) + 'BA'
                mezo_delivery_date_xml.attrib['eazon'] = mezo_delivery_date_xml_eazon
                mezo_delivery_date_xml.text = str(partner_invoice.date).replace("-", "")
                mezok_xml.append(mezo_delivery_date_xml)

                # mezo_net_total_xml 0B0001C0001CA
                mezo_net_total_xml = lxml.etree.Element('mezo')
                mezo_net_total_xml_eazon = '0B0001C000' + str(invoice_index) + 'CA'
                mezo_net_total_xml.attrib['eazon'] = mezo_net_total_xml_eazon
                if partner_invoice.l10n_hu_invoice:
                    net_total_nav_value = partner_invoice.l10n_hu_invoice.invoice_net_amount_huf / 1000
                else:
                    net_total_nav_value = abs(partner_invoice.amount_untaxed_signed / 1000)
                net_total_nav_value_rounded_int = int(round(net_total_nav_value, 0))
                mezo_net_total_xml.text = str(net_total_nav_value_rounded_int)
                mezok_xml.append(mezo_net_total_xml)

                # mezo_vat_total_xml
                mezo_vat_total_xml = lxml.etree.Element('mezo')
                mezo_vat_total_xml_eazon = '0B0001C000' + str(invoice_index) + 'DA'
                mezo_vat_total_xml.attrib['eazon'] = mezo_vat_total_xml_eazon
                if partner_invoice.l10n_hu_invoice:
                    vat_total_nav_value = partner_invoice.l10n_hu_invoice.invoice_vat_amount_huf / 1000
                else:
                    vat_total_nav_value = abs(partner_invoice.amount_tax_signed / 1000)
                vat_total_nav_value_rounded_int = int(round(vat_total_nav_value, 0))
                mezo_vat_total_xml.text = str(vat_total_nav_value_rounded_int)
                mezok_xml.append(mezo_vat_total_xml)

            nyomtatvany_xml.append(mezok_xml)
            # END MEZOK

            # Append nyomtatvany to nyomtatvanyok
            nyomtatvanyok_xml.append(nyomtatvany_xml)

        # attachment
        # Make a string
        nyomtatvanyok_xml_string = lxml.etree.tostring(
            nyomtatvanyok_xml,
            # xml_declaration=True,
            doctype='<?xml version="1.0" encoding="utf-8"?>',
            # encoding="utf-8",
            # method="xml",
            pretty_print=True,
            # with_tail=False,
        )
        # nyomtatvanyok_xml_string_quotes = nyomtatvanyok_xml_string.replace("'", '"')
        # nyomtatvanyok_xml_base64 = base64.b64encode(nyomtatvanyok_xml_string_quotes)
        nyomtatvanyok_xml_base64 = base64.b64encode(nyomtatvanyok_xml_string)
        attachment_datas = nyomtatvanyok_xml_base64

        attachment_name = str(template_code)
        attachment_name += self.company.partner_id.l10n_hu_vat
        attachment_name += "_"
        attachment_name += str(fields.Datetime.now()).replace(':', '_').replace(' ', '_')
        attachment_name += ".xml"

        xml_attachment_values = {
            'name': attachment_name,
            'type': 'binary',
            'datas': attachment_datas,
            'mimetype': 'application/xml',
            'res_model': 'l10n.hu.nav.report',
            'res_id': self.id,
            'res_name': self.display_name
        }
        # Create attachment
        self.env['ir.attachment'].create(xml_attachment_values)

        # Return
        return result

    @api.model
    def run_report(self, values):
        """ Run report """
        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        inputs = []
        input_ids = []
        outputs = []
        output_ids = []
        result = {}
        warning_list = []

        # Delete unlocked existing inputs
        self.env['l10n.hu.nav.report.input'].sudo().search([
            ('locked', '=', False),
            ('report', '=', self.id),
        ]).unlink()

        # Delete unlocked existing outputs
        self.env['l10n.hu.nav.report.output'].sudo().search([
            ('locked', '=', False),
            ('report', '=', self.id),
        ]).unlink()

        # Prepare inputs and outputs
        if self.template:
            # INPUTS
            inputs_result = self.get_report_input_values({})
            error_list += inputs_result.get('error_list', [])
            if inputs_result.get('input_values_list'):
                for input_values in inputs_result['input_values_list']:
                    new_input = self.env['l10n.hu.nav.report.input'].create(input_values)
                    inputs.append(new_input)
                    input_ids.append(new_input.id)

            # OUTPUTS
            outputs_result = self.get_report_output_values({})
            error_list += outputs_result.get('error_list', [])
            if outputs_result.get('output_values_list'):
                for output_values in outputs_result['output_values_list']:
                    new_output = self.env['l10n.hu.nav.report.output'].create(output_values)
                    outputs.append(new_output)
                    output_ids.append(new_output.id)
        else:
            pass

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'inputs': inputs,
            'input_ids': input_ids,
            'outputs': outputs,
            'output_ids': output_ids,
            'warning_list': warning_list,
        })

        # Return
        return result

    # # HELPER
    @api.model
    def get_nav_report_company_name(self):
        """ Can be called from input to get company name

        :return: string
        """
        return self.company.name

    @api.model
    def get_nav_report_company_tax_number(self):
        """ Can be called from input to get company name

        :return: string
        """
        return self.company.partner_id.l10n_hu_vat.replace("-", "")

    @api.model
    def get_report_input_values(self, values):
        """ Get input values for a report """
        # raise exceptions.UserError("get_report_input_values BEGIN" + str(values))
        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        input_values_list = []
        result = {}
        warning_list = []

        # Get input rules
        rules = self.env['l10n.hu.nav.report.rule'].sudo().search([
            ('company', '=', self.company.id),
            ('report_template', '=', self.template.id),
            ('rule_type', '=', 'report_input'),
        ])
        # raise exceptions.UserError(str(len(rules)))

        # Iterate rules
        for rule in rules:
            # Common values
            input_values_common = {
                'locked': rule.report_data_locked,
                'name': rule.name,
                'rule': rule.id,
                'report': self.id,
            }
            if rule.report_data_category:
                input_values_common.update({
                    'category': rule.report_data_category.id,
                })
            if rule.technical_name == 'company_name':
                company_name = self.get_nav_report_company_name()
                input_values = {
                    'partner': self.company.partner_id.id,
                    'value_char': company_name,
                }
                input_values.update(input_values_common)
                input_values_list.append(input_values)
            elif rule.technical_name == 'company_tax_number':
                company_tax_number = self.get_nav_report_company_tax_number()
                input_values = {
                    'partner': self.company.partner_id.id,
                    'value_char': company_tax_number,
                }
                input_values.update(input_values_common)
                input_values_list.append(input_values)
            elif rule.technical_name == 'account_move_line':
                # Base domain
                aml_domain = [
                    ('l10n_hu_move_vat_date', '>=', self.period_start),
                    ('l10n_hu_move_vat_date', '<=', self.period_end),
                    ('move_id.state', '=', 'posted'),
                ]

                # Custom domain
                if rule.account_move_line_domain and len(rule.account_move_line_domain) > 0:
                    try:
                        aml_domain += safe_eval(rule.account_move_line_domain)
                    except:
                        pass

                # DO search
                relevant_account_move_lines = self.env['account.move.line'].search(aml_domain)

                for account_move_line in relevant_account_move_lines:
                    # ACCOUNTING
                    # # fiscal position
                    if account_move_line.move_id.fiscal_position_id:
                        account_fiscal_position_id = account_move_line.move_id.fiscal_position_id.id
                    else:
                        account_fiscal_position_id = False

                    # # tax scope
                    account_tax_scope = False
                    if account_move_line.tax_line_id:
                        if account_move_line.tax_line_id.tax_scope == 'consu':
                            account_tax_scope = 'product'
                        elif account_move_line.tax_line_id.tax_scope == 'service':
                            account_tax_scope = 'service'
                        else:
                            pass
                    elif account_move_line.tax_ids:
                        # Initialize
                        tax_scopes = []
                        tax_scope_empty_count = 0

                        # Inspect
                        for tax_id in account_move_line.tax_ids:
                            if tax_id.tax_scope and tax_id.tax_scope not in tax_scopes:
                                tax_scopes.append(tax_id.tax_scope)
                            else:
                                tax_scope_empty_count += 1

                        # Evaluate
                        if len(tax_scopes) == 1 and tax_scope_empty_count == 0:
                            if tax_scopes[0] == 'consu':
                                account_tax_scope = 'product'
                            elif tax_scopes[0] == 'service':
                                account_tax_scope = 'service'
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass

                    # PARTNER
                    partner = account_move_line.move_id.partner_id.commercial_partner_id
                    partner_name = partner.name

                    # # Partner country
                    if partner.country_id:
                        partner_country_code = partner.country_id.code
                        partner_country_id = partner.country_id.id
                    else:
                        partner_country_code = False
                        partner_country_id = False

                    # # Partner tax number
                    if partner.l10n_hu_vat:
                        partner_tax_number = partner.l10n_hu_vat
                    elif partner.vat:
                        partner_tax_number = partner.vat
                    else:
                        partner_tax_number = False

                    # # Partner tax unit
                    if partner.l10n_hu_tax_unit:
                        partner_tax_unit = partner.l10n_hu_tax_unit
                        partner_tax_unit_id = partner_tax_unit.id
                    else:
                        partner_tax_unit = False
                        partner_tax_unit_id = False

                    # # Tax number
                    if partner_tax_unit and partner_tax_unit.l10n_hu_vat:
                        tax_number = partner_tax_unit.l10n_hu_vat
                    elif partner_tax_unit and partner_tax_unit.vat:
                        tax_number = partner_tax_unit.vat
                    elif partner_tax_number:
                        tax_number = partner_tax_number
                    else:
                        tax_number = False

                    # # Partner positions
                    if partner.property_account_position_id:
                        partner_fiscal_position_id = partner.property_account_position_id.id
                        partner_trade_position = partner.property_account_position_id.l10n_hu_trade_position
                    else:
                        partner_fiscal_position_id = False
                        partner_trade_position = False

                    # Fiscal position match
                    if account_fiscal_position_id == partner_fiscal_position_id:
                        fiscal_position_match = True
                    else:
                        fiscal_position_match = False

                    # PRODUCT
                    product_id = False
                    product_code = False
                    product_name = False
                    product_scope = False
                    product_type = False
                    product_uom_id = False
                    product_uom_name = False
                    product_uom_category_id = False
                    product_uom_category_name = False
                    product_uom_type = False
                    if account_move_line.product_id:
                        product_id = account_move_line.product_id.id
                        product_code = account_move_line.product_id.default_code
                        product_name = account_move_line.product_id.name
                        product_scope = account_move_line.product_id.l10n_hu_get_nav_report_product_scope()
                        product_type = account_move_line.product_id.detailed_type
                        product_uom_id = account_move_line.product_uom_id.id
                        product_uom_category_id = account_move_line.product_uom_category_id.id
                        product_uom_category_name = account_move_line.product_uom_category_id.name
                        product_uom_name = account_move_line.product_uom_id.name
                        product_uom_type = account_move_line.product_uom_id.l10n_hu_type

                    input_values = {
                        'account_fiscal_position': account_fiscal_position_id,
                        'account_move': account_move_line.move_id.id,
                        'account_move_line': account_move_line.id,
                        'account_tag': [(4, x.id, 0) for x in account_move_line.tax_tag_ids],
                        'account_tag_invert': account_move_line.tax_tag_invert,
                        'account_tax': [(4, x.id, 0) for x in account_move_line.tax_ids],
                        'account_tax_line': account_move_line.tax_line_id.id,
                        'account_tax_scope': account_tax_scope,
                        'amount_balance': account_move_line.balance,
                        'amount_currency': account_move_line.amount_currency,
                        'amount_credit': account_move_line.credit,
                        'amount_debit': account_move_line.debit,
                        'currency': account_move_line.currency_id.id,
                        'currency_code': account_move_line.currency_id.name,
                        'currency_rate': account_move_line.currency_rate,
                        'delivery_date': account_move_line.date,
                        'downpayment': account_move_line.is_downpayment,
                        'fiscal_position_match': fiscal_position_match,
                        'payment_date': account_move_line.date_maturity,
                        'partner': partner.id,
                        'partner_country': partner_country_id,
                        'partner_country_code': partner_country_code,
                        'partner_name': partner_name,
                        'partner_fiscal_position': partner_fiscal_position_id,
                        'partner_tax_number': partner_tax_number,
                        'partner_tax_unit': partner_tax_unit_id,
                        'partner_trade_position': partner_trade_position,
                        'product': product_id,
                        'product_code': product_code,
                        'product_name': product_name,
                        'product_scope': product_scope,
                        'product_type': product_type,
                        'product_uom_category': product_uom_category_id,
                        'product_uom_category_name': product_uom_category_name,
                        'product_uom': product_uom_id,
                        'product_uom_name': product_uom_name,
                        'product_uom_type': product_uom_type,
                        'tax_number': tax_number,
                    }

                    input_values.update(input_values_common)
                    if account_move_line.tax_audit:
                        input_values.update({
                            'name': account_move_line.tax_audit
                        })
                    input_values_list.append(input_values)
            elif rule.technical_name == 'customer_invoice':
                # Base domain
                cs_domain = [
                    ('l10n_hu_vat_date', '>=', self.period_start),
                    ('l10n_hu_vat_date', '<=', self.period_end),
                    ('move_type', 'in', ['out_invoice', 'out_refund', 'out_receipt']),
                    ('state', '=', 'posted'),
                ]

                # Custom domain
                if rule.account_move_domain and len(rule.account_move_domain) > 0:
                    try:
                        cs_domain += safe_eval(rule.account_move_domain)
                    except:
                        pass

                # DO search
                customer_invoices = self.env['account.move'].search(cs_domain)

                for customer_invoice in customer_invoices:
                    input_values = {
                        'account_move': customer_invoice.id,
                        'amount_net': customer_invoice.amount_untaxed,
                        'amount_tax': customer_invoice.amount_tax,
                        'amount_total': customer_invoice.amount_total,
                        'partner': customer_invoice.partner_id.id,
                        'value_date': customer_invoice.date,
                    }
                    input_values.update(input_values_common)
                    input_values_list.append(input_values)
            elif rule.technical_name == 'vendor_bill':
                # Base domain
                vb_domain = [
                    ('l10n_hu_vat_date', '>=', self.period_start),
                    ('l10n_hu_vat_date', '<=', self.period_end),
                    ('move_type', 'in', ['in_invoice', 'in_refund', 'in_receipt']),
                    ('state', '=', 'posted'),
                ]

                # Custom domain
                if rule.account_move_domain and len(rule.account_move_domain) > 0:
                    try:
                        vb_domain += safe_eval(rule.account_move_domain)
                    except:
                        pass

                # DO search
                vendor_bills = self.env['account.move'].search(vb_domain)

                for vendor_bill in vendor_bills:
                    input_values = {
                        'account_move': vendor_bill.id,
                        'amount_net': vendor_bill.amount_untaxed,
                        'amount_tax': vendor_bill.amount_tax,
                        'amount_total': vendor_bill.amount_total,
                        'partner': vendor_bill.partner_id.id,
                        'value_date': vendor_bill.date,
                    }
                    input_values.update(input_values_common)
                    input_values_list.append(input_values)
            else:
                pass

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'input_values_list': input_values_list,
            'warning_list': warning_list,
        })

        # Return
        # raise exceptions.UserError("get_report_input_values END" + str(result))
        return result

    @api.model
    def get_report_output_values(self, values):
        """ Get output values for a report

        NOTE:
        - Inputs are prepared at this point

        @param values: dictionary

        @return: dictionary
        """
        # raise exceptions.UserError("get_report_output_values BEGIN" + str(values))
        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        output_values_list = []
        result = {}
        warning_list = []

        # Prepare output from elements
        for element in self.template.element:
            # 1) prepare output_values
            if element.code:
                output_code = element.code
            elif element.nav_code:
                output_code = element.nav_code
            else:
                output_code = False

            if element.technical_name:
                output_technical_name = element.technical_name
            elif element.nav_eazon:
                output_technical_name = element.nav_eazon
            else:
                output_technical_name = False

            # value_type
            if element.output_method == 'rule':
                value_type = element.output_rule.value_type
            else:
                value_type = element.value_type

            output_values = {
                'code': output_code,
                'element': element.id,
                'locked': element.output_locked,
                'name': element.name,
                'report': self.id,
                'technical_name': output_technical_name,
                'template': self.template.id,
                'value_type': value_type,
            }

            # 2) get output value
            if element.input_method == 'rule':
                # Initialize output_value
                if value_type == 'float':
                    output_value = 0.0
                elif value_type == 'integer':
                    output_value = 0
                else:
                    output_value = False

                # Prepare domain
                domain = [
                    ('report', '=', self.id),
                    ('rule', '=', element.input_rule.id),
                ]
                try:
                    domain += safe_eval(element.input_domain)
                except:
                    pass

                # Collect data
                recordset = self.env['l10n.hu.nav.report.input'].search(domain)

                for record in recordset:
                    if value_type == 'float':
                        output_value += record[element.output_rule.ir_model_field_name]
                    elif value_type == 'integer':
                        output_value += record[element.output_rule.ir_model_field_name]
                    else:
                        pass

                # Update values
                if value_type == 'float':
                    output_values.update({
                        'value_float': output_value,
                    })
                elif value_type == 'integer':
                    output_values.update({
                        'value_integer': output_value,
                    })
                else:
                    pass
                # raise exceptions.UserError("rule output_values" + str(output_values))
            else:
                pass

            # Append to list
            output_values_list.append(output_values)

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'output_values_list': output_values_list,
            'warning_list': warning_list,
        })

        # Return
        # raise exceptions.UserError("get_report_output_values END" + str(result))
        return result
