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
    template = fields.Many2one(
        comodel_name='l10n.hu.nav.report.template',
        index=True,
        required=True,
        string="Template",
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
            name = "NAV-REP-" + str(record.id)

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

    def action_wizard_report(self):
        """ Start report wizard """
        # Ensure one record in self
        self.ensure_one()

        # Assemble context
        context = {
            'default_action_nav_report': 'run_report',
            'default_action_nav_report_editable': True,
            'default_action_nav_report_required': True,
            'default_action_nav_report_visible': True,
            'default_action_type': 'nav_report',
            'default_action_type_editable': False,
            'default_action_type_visible': False,
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
        if self.template and self.template.code == '2365A':
            result = self.print_report_xml_2365a(values)

        # Return
        return result

    @api.model
    def print_report_xml_2365a(self, values):
        """ Print 2365A report as xml """
        result = {}

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
        nyomtatvanyazonosito_xml.text = str("2365A")
        nyomtatvanyinformacio_xml.append(nyomtatvanyazonosito_xml)

        # nyomtatvanyverzio_xml
        nyomtatvanyverzio_xml = lxml.etree.Element('nyomtatvanyverzio')
        nyomtatvanyverzio_xml.text = str("1.0")
        nyomtatvanyinformacio_xml.append(nyomtatvanyverzio_xml)

        # adozo_xml
        adozo_xml = lxml.etree.Element('adozo')

        # adozo_nev_xml
        adozo_nev_xml = lxml.etree.Element('nev')
        adozo_nev_xml.text = str(self.company.partner_id.name)
        adozo_xml.append(adozo_nev_xml)

        # adozo_adoszam_xml
        adozo_adoszam_xml = lxml.etree.Element('adoszam')
        adozo_adoszam_raw = str(self.company.partner_id.oregional_l10n_hu_vat)
        adozo_adoszam_xml.text = adozo_adoszam_raw.replace("-", "")
        adozo_xml.append(adozo_adoszam_xml)

        nyomtatvanyinformacio_xml.append(adozo_xml)
        nyomtatvany_xml.append(nyomtatvanyinformacio_xml)

        # mezok_xml
        mezok_xml = lxml.etree.Element('mezok')

        # process outputs
        for output in self.output:
            if print_locked and output.is_locked:
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
            ('oregional_invoice_delivery_date', '>=', self.period_start),
            ('oregional_invoice_delivery_date', '<=', self.period_end),
            ('partner_id.commercial_partner_id.oregional_l10n_hu_vat', '!=', False),
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
                ('oregional_invoice_delivery_date', '>=', self.period_start),
                ('oregional_invoice_delivery_date', '<=', self.period_end),
                ('partner_id', '=', relevant_partner.id),
            ])

            # nyomtatvany_xml
            nyomtatvany_xml = lxml.etree.Element('nyomtatvany')

            # BEGIN NYOMTATVANYINFORMACIO
            # nyomtatvanyinformacio_xml
            nyomtatvanyinformacio_xml = lxml.etree.Element('nyomtatvanyinformacio')

            # nyomtatvanyazonosito_xml
            nyomtatvanyazonosito_xml = lxml.etree.Element('nyomtatvanyazonosito')
            nyomtatvanyazonosito_xml.text = str("2365M")
            nyomtatvanyinformacio_xml.append(nyomtatvanyazonosito_xml)

            # nyomtatvanyverzio_xml
            nyomtatvanyverzio_xml = lxml.etree.Element('nyomtatvanyverzio')
            nyomtatvanyverzio_xml.text = str("1.0")
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
            adozo_adoszam_raw = str(self.company.partner_id.oregional_l10n_hu_vat)
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
            albizonylatazonositas_azonosito_xml.text = str(relevant_partner.oregional_l10n_hu_vat[:8])
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
                mezo_delivery_date_xml.text = str(partner_invoice.l10n_hu_invoice_delivery_date).replace("-", "")
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
                if partner_invoice.oregional_nav_invoice:
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

        attachment_name = "2365a_"
        attachment_name += self.company.partner_id.oregional_l10n_hu_vat
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
        result = {}

        # Delete unlocked existing inputs
        self.env['l10n.hu.nav.report.input'].sudo().search([
            ('report', '=', self.id),
            ('is_locked', '=', False),
        ]).unlink()

        # Delete unlocked existing outputs
        self.env['l10n.hu.nav.report.output'].sudo().search([
            ('report', '=', self.id),
            ('is_locked', '=', False),
        ]).unlink()

        if self.template and self.template.code == '2365A':
            result = self.run_report_2365a(values)

        # Return
        return result

    @api.model
    def run_report_2365a(self, values):
        """ Run report VAT 2365A """
        inputs = []
        outputs = []
        result = {}
        value_rules = []

        # Prepare raw input-output values
        for element in self.template.element:
            if element.value_rule and element.value_rule not in value_rules:
                # create raw_input
                new_input_values = {
                    'rule': element.value_rule.id,
                    'name': element.value_rule.name,
                    'report': self.id,
                }
                new_input = self.env['l10n.hu.nav.report.input'].create(new_input_values)
                inputs.append(new_input)
                value_rules.append(element.value_rule)

            # output_code
            if element.code:
                output_code = element.code
            elif element.nav_code:
                output_code = element.nav_code
            else:
                output_code = False

            # output_technical_name
            if element.technical_name:
                output_technical_name = element.technical_name
            elif element.nav_eazon:
                output_technical_name = element.nav_eazon
            else:
                output_technical_name = False

            new_output_values = {
                'code': output_code,
                'element': element.id,
                'name': element.name,
                'report': self.id,
                'technical_name': output_technical_name,
                'template': self.template.id,
                'value_type': element.value_type,
            }
            new_output = self.env['l10n.hu.nav.report.output'].create(new_output_values)
            outputs.append(new_output)

        # Compute inputs

        # Compute outputs

        # Return
        return result
