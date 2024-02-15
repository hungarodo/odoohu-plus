# -*- coding: utf-8 -*-
# 1 : imports of python lib
import base64
import datetime
import json
import re

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.addons.l10n_hu_base.models import l10n_hu_amount_to_text

# 4 : variable declarations


# Class
class L10nHuAccountInvoice(models.Model):
    # Private attributes
    _name = 'l10n.hu.invoice'
    _description = "HU Invoice"
    _order = 'write_date desc, id desc'

    # Default methods

    # Field declarations
    # # Base fields
    account_journal = fields.Many2one(
        comodel_name='account.journal',
        copy=False,
        index=True,
        readonly=True,
        string="Journal",
    )
    account_move = fields.Many2one(
        comodel_name='account.move',
        copy=False,
        ondelete='cascade',
        string="Account Move",
    )
    account_move_status = fields.Selection(
        related='account_move.state',
        store=True,
        string="Account Move Status",
    )
    account_move_type = fields.Selection(
        related='account_move.move_type',
        index=True,
        store=True,
        string="Account Move Type",
    )
    amount_untaxed = fields.Float(
        copy=False,
        readonly=True,
        string="Net Amount",
    )
    amount_tax = fields.Float(
        copy=False,
        readonly=True,
        string="Tax Amount",
    )
    amount_total = fields.Float(
        copy=False,
        readonly=True,
        string="Gross Amount",
    )
    comment = fields.Char(
        copy=False,
        readonly=True,
        string="Comment",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        copy=False,
        readonly=True,
        string="Company",
    )
    company_currency = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Company Currency",
    )
    company_currency_name = fields.Char(
        copy=False,
        readonly=True,
        string="Company Currency Name",
    )
    currency = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Currency",
    )
    currency_huf = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Currency HUF",
    )
    currency_rate = fields.Many2one(
        comodel_name='res.currency.rate',
        copy=False,
        readonly=True,
        string="Currency Rate",
    )
    currency_rate_date = fields.Char(
        copy=False,
        readonly=True,
        string="Currency Rate Date",
    )
    currency_rate_amount = fields.Float(
        copy=False,
        readonly=True,
        string="Currency Rate Amount",
    )
    currency_rate_huf = fields.Many2one(
        comodel_name='res.currency.rate',
        copy=False,
        readonly=True,
        string="Currency Rate HUF",
    )
    currency_rate_huf_date = fields.Char(
        copy=False,
        readonly=True,
        string="Currency Rate HUF Date",
    )
    currency_rate_huf_amount = fields.Float(
        copy=False,
        readonly=True,
        string="Currency Rate HUF Amount",
    )
    currency_symbol = fields.Char(
        copy=False,
        readonly=True,
        string="Currency Symbol",
    )
    document_type = fields.Many2one(
        comodel_name='l10n.hu.document.type',
        copy=False,
        readonly=True,
        string="Document Type",
    )
    document_type_name = fields.Char(
        copy=False,
        readonly=True,
        string="Document Type Name",
    )
    eu_oss_eligible = fields.Boolean(
        copy=False,
        default=False,
        readonly=True,
        string="EU OSS Eligible",
    )
    eu_oss_enabled = fields.Boolean(
        copy=False,
        default=False,
        readonly=True,
        string="EU OSS Enabled",
    )
    fiscal_position = fields.Many2one(
        comodel_name='account.fiscal.position',
        copy=False,
        readonly=True,
        string="Fiscal Position",
    )
    fiscal_position_name = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Position Name",
    )
    file_json = fields.Binary(
        copy=False,
        readonly=True,
        string="JSON File",
    )
    file_pdf = fields.Binary(
        copy=False,
        readonly=True,
        string="PDF File",
    )
    file_xml = fields.Binary(
        copy=False,
        readonly=True,
        string="XML File",
    )
    invoice_category = fields.Selection(
        copy=False,
        readonly=True,
        selection=[
            ('normal', "Normal"),
            ('simplified', "Simplified"),
            ('aggregate', "Aggregate"),
        ],
        string="Invoice Category",
    )
    invoice_line = fields.One2many(
        comodel_name='l10n.hu.invoice.line',
        inverse_name='invoice',
        copy=False,
        readonly=True,
        string="Invoice Line",
    )
    invoice_line_count = fields.Integer(
        copy=False,
        string="Invoice Line Count",
    )
    invoice_log = fields.One2many(
        comodel_name='l10n.hu.invoice.log',
        copy=False,
        index=True,
        inverse_name='invoice',
        string="Invoice Log",
    )
    invoice_log_count = fields.Integer(
        compute='_compute_invoice_log_count',
        string="Invoice Log Count",
    )
    invoice_operation = fields.Char(
        copy=False,
        readonly=True,
        string="Invoice Operation",
    )
    invoice_type = fields.Char(
        copy=False,
        readonly=True,
        string="Invoice Type",
    )
    is_foreign_currency = fields.Boolean(
        copy=False,
        help="The invoice is in foreign currency",
        readonly=True,
        string="Foreign Currency",
    )
    is_locked = fields.Boolean(
        copy=False,
        default=False,
        string="Locked",
    )
    maintenance_data = fields.Text(
        copy=False,
        readonly=True,
        string="Maintenance Data",
    )
    maintenance_status = fields.Char(
        copy=False,
        readonly=True,
        string="Maintenance Status",
    )
    maintenance_timestamp = fields.Datetime(
        copy=False,
        readonly=True,
        string="Maintenance Timestamp",
    )
    modification_index = fields.Integer(
        copy=False,
        readonly=True,
        string="Modification Index",
    )
    modify_without_master = fields.Boolean(
        copy=False,
        readonly=True,
        string="Modify Without Master",
    )
    original_account_move = fields.Many2one(
        related='original_invoice.account_move',
        index=True,
        store=True,
        string="Original Account Move",
    )
    original_invoice = fields.Many2one(
        copy=False,
        comodel_name='l10n.hu.invoice',
        readonly=True,
        string="Original Invoice",
    )
    original_invoice_number = fields.Char(
        copy=False,
        readonly=True,
        string="Original Invoice Number",
    )
    payment_term = fields.Many2one(
        comodel_name='account.payment.term',
        copy=False,
        readonly=True,
        string="Payment Term",
    )
    product_charge_sum = fields.Monetary(
        currency_field='currency_huf',
        string="Product Charge Sum",
    )
    product_fee_operation = fields.Selection(
        selection=[
            ('deposit', "Deposit"),
            ('refund', "Refund"),
        ],
        string="Product Fee Operation",
    )
    product_fee_summary = fields.One2many(
        comodel_name='l10n.hu.invoice.product.fee',
        domain=[('scope', '=', 'summary')],
        inverse_name='invoice',
        string="Product Fee Summary",
    )
    reference = fields.Char(
        compute='_compute_reference',
        string="Reference",
    )
    technical_source = fields.Char(
        copy=False,
        readonly=True,
        string="Technical Source",
    )
    technical_type = fields.Char(
        copy=False,
        readonly=True,
        string="Technical Type",
    )
    # # invoiceHead supplierInfo
    supplier = fields.Many2one(
        comodel_name='res.partner',
        copy=False,
        index=True,
        readonly=True,
        string="Supplier",
    )
    supplier_address_building = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Building",
    )
    supplier_address_country = fields.Many2one(
        comodel_name='res.country',
        copy=False,
        index=True,
        readonly=True,
        string="Supplier Country",
    )
    supplier_address_country_code = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Country Code",
    )
    supplier_address_country_name = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Country Name",
    )
    supplier_address_country_state_code = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Country State Code",
    )
    supplier_address_country_state_name = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Country State Name",
    )
    supplier_address_district = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address District",
    )
    supplier_address_door = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Door",
    )
    supplier_address_floor = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Floor",
    )
    supplier_address_house_number = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address House Number",
    )
    supplier_address_lot_number = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Lot Number",
    )
    supplier_address_postal_code = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Postal Code",
    )
    supplier_address_public_place_name = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Public Place Name",
    )
    supplier_address_public_place_type = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Public Place Type",
    )
    supplier_address_settlement = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Settlement",
    )
    supplier_address_staircase = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Staircase",
    )
    supplier_address_street = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Street",
    )
    supplier_address_street2 = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Street2",
    )
    supplier_address_type = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Address Type",
    )
    supplier_bank_account = fields.Many2one(
        comodel_name='res.partner.bank',
        copy=False,
        readonly=True,
        string="Supplier Bank Account",
    )
    supplier_bank_account_number = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Bank Account Number",
    )
    supplier_community_vat_number = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Community Vat Number",
    )
    supplier_excise_license_number = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Excise License Number",
    )
    supplier_is_cash_accounting = fields.Boolean(
        copy=False,
        readonly=True,
        string="Supplier Cash Accounting",
    )
    supplier_is_individual_exemption = fields.Boolean(
        copy=False,
        readonly=True,
        string="Supplier Individual Exemption",
    )
    supplier_is_l10n_hu = fields.Boolean(
        copy=False,
        readonly=True,
        string="Supplier Hungarian",
    )
    supplier_is_personal_tax_exempt = fields.Boolean(
        copy=False,
        readonly=True,
        string="Supplier Personal Tax Exempt",
    )
    supplier_is_self_billing = fields.Boolean(
        copy=False,
        readonly=True,
        string="Supplier Self Billing",
    )
    supplier_is_self_employed = fields.Boolean(
        copy=False,
        readonly=True,
        string="Supplier Self-Employed",
    )
    supplier_is_small_business = fields.Boolean(
        copy=False,
        readonly=True,
        string="Supplier Small Business",
    )
    supplier_is_vat_reverse_charge = fields.Boolean(
        copy=False,
        readonly=True,
        string="Supplier VAT Reverse Charge",
    )
    supplier_l10n_hu_crn = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier HU CRN",
    )
    supplier_name = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Name",
    )
    supplier_incorporation = fields.Selection(
        copy=False,
        selection=[
            ('organization', "Organization"),
            ('self_employed', "Self Employed"),
            ('taxable_person', "Taxable Person"),
        ],
        index=True,
        readonly=True,
        string="Supplier Taxpayer Type",
    )
    supplier_vat_status = fields.Selection(
        copy=False,
        selection=[
            ('domestic', "Domestic"),
            ('private_person', "Private Person"),
            ('other', "Other"),
        ],
        index=True,
        readonly=True,
        string="Supplier VAT Status",
    )
    supplier_self_employed_name = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Self-Employed Name",
    )
    supplier_self_employed_number = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Self-Employed Number",
    )
    supplier_tax_number = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier Tax Number",
    )
    supplier_vat_domestic_reverse_charge = fields.Boolean(
        copy=False,
        readonly=True,
        string="Supplier VAT Domestic Reverse Charge",
    )
    """ VAT GROUP
    supplier_vat_group = fields.Many2one(
        comodel_name='l10n_hu.l10n.hu.vat.group',
        copy=False,
        readonly=True,
        string="Supplier VAT Group",
    )
    supplier_vat_group_number = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier VAT Group Number",
    )
    supplier_vat_group_member_number = fields.Char(
        copy=False,
        readonly=True,
        string="Supplier VAT Group Member Number",
    )
    """
    # # invoiceHead customerInfo
    customer = fields.Many2one(
        comodel_name='res.partner',
        copy=False,
        index=True,
        readonly=True,
        string="Customer",
    )
    customer_address_building = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Building",
    )
    customer_address_country = fields.Many2one(
        comodel_name='res.country',
        copy=False,
        index=True,
        readonly=True,
        string="Customer Country",
    )
    customer_address_country_code = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Country Code",
    )
    customer_address_country_name = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Country Name",
    )
    customer_address_country_state_code = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Country State Code",
    )
    customer_address_country_state_name = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Country State Name",
    )
    customer_address_district = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address District",
    )
    customer_address_door = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Door",
    )
    customer_address_floor = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Floor",
    )
    customer_address_house_number = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address House Number",
    )
    customer_address_lot_number = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Lot Number",
    )
    customer_address_postal_code = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Postal Code",
    )
    customer_address_public_place_name = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Public Place Name",
    )
    customer_address_public_place_type = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Public Place Type",
    )
    customer_address_settlement = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Settlement",
    )
    customer_address_staircase = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Staircase",
    )
    customer_address_street = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Street",
    )
    customer_address_street2 = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Street2",
    )
    customer_address_type = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Address Type",
    )
    customer_bank_account = fields.Many2one(
        comodel_name='res.partner.bank',
        copy=False,
        readonly=True,
        string="Customer Bank Account",
    )
    customer_bank_account_number = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Bank Account Number",
    )
    customer_community_vat_number = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Community VAT Number",
    )
    customer_fiscal_position = fields.Many2one(
        comodel_name='account.fiscal.position',
        copy=False,
        readonly=True,
        string="Customer Fiscal Position",
    )
    customer_fiscal_position_name = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Fiscal Position Name",
    )
    customer_is_cash_accounting = fields.Boolean(
        copy=False,
        readonly=True,
        string="Customer Cash Accounting",
    )
    customer_is_l10n_hu = fields.Boolean(
        copy=False,
        readonly=True,
        string="Hungarian",
    )
    customer_is_personal_tax_exempt = fields.Boolean(
        copy=False,
        readonly=True,
        string="Customer Personal Tax Exempt",
    )
    customer_is_self_billing = fields.Boolean(
        copy=False,
        readonly=True,
        string="Customer Self Billing",
    )
    customer_is_small_business = fields.Boolean(
        copy=False,
        readonly=True,
        string="Customer Small Business",
    )
    customer_is_vat_reverse_charge = fields.Boolean(
        copy=False,
        readonly=True,
        string="Customer VAT Reverse Charge",
    )
    customer_l10n_hu_crn = fields.Char(
        copy=False,
        readonly=True,
        string="Customer CRN",
    )
    customer_name = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Name",
    )
    customer_incorporation = fields.Selection(
        copy=False,
        selection=[
            ('organization', "Organization"),
            ('self_employed', "Self Employed"),
            ('taxable_person', "Taxable Person"),
        ],
        index=True,
        readonly=True,
        string="Customer Taxpayer Type",
    )
    customer_vat_status = fields.Selection(
        copy=False,
        selection=[
            ('domestic', "Domestic"),
            ('private_person', "Private Person"),
            ('other', "Other"),
        ],
        index=True,
        readonly=True,
        string="Customer VAT Status",
    )
    customer_tax_number = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Tax Number",
    )
    customer_third_state_tax_id = fields.Char(
        copy=False,
        readonly=True,
        string="Customer Third State Tax ID",
    )
    """ VAT GROUP
    customer_vat_group = fields.Many2one(
        comodel_name='l10n_hu.l10n.hu.vat.group',
        copy=False,
        readonly=True,
        string="Customer VAT Group",
    )
    customer_vat_group_number = fields.Char(
        copy=False,
        readonly=True,
        string="Customer VAT Group Number",
    )
    customer_vat_group_member_number = fields.Char(
        copy=False,
        readonly=True,
        string="Customer VAT Group Member Number",
    )
    """
    # # invoiceHead fiscalRepresentativeInfo
    fiscal_representative = fields.Many2one(
        comodel_name='res.partner',
        copy=False,
        index=True,
        readonly=True,
        string="Fiscal Representative",
    )
    fiscal_representative_address_building = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Building",
    )
    fiscal_representative_address_country = fields.Many2one(
        comodel_name='res.country',
        copy=False,
        index=True,
        readonly=True,
        string="Fiscal Representative Country",
    )
    fiscal_representative_address_country_code = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Country Code",
    )
    fiscal_representative_address_country_name = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Country Name",
    )
    fiscal_representative_address_country_state_code = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Country State Code",
    )
    fiscal_representative_address_country_state_name = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Country State Name",
    )
    fiscal_representative_address_district = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address District",
    )
    fiscal_representative_address_door = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Door",
    )
    fiscal_representative_address_floor = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Floor",
    )
    fiscal_representative_address_house_number = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address House Number",
    )
    fiscal_representative_address_level = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Level",
    )
    fiscal_representative_address_lot_number = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Lot Number",
    )
    fiscal_representative_address_postal_code = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Postal Code",
    )
    fiscal_representative_address_public_place_name = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Public Place Name",
    )
    fiscal_representative_address_public_place_type = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Public Place Type",
    )
    fiscal_representative_address_settlement = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Settlement",
    )
    fiscal_representative_address_staircase = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Staircase",
    )
    fiscal_representative_address_street = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Street",
    )
    fiscal_representative_address_street2 = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Street2",
    )
    fiscal_representative_address_type = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Address Type",
    )
    fiscal_representative_bank_account = fields.Many2one(
        comodel_name='res.partner.bank',
        copy=False,
        readonly=True,
        string="Fiscal Representative Bank Account",
    )
    fiscal_representative_bank_account_number = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Bank Account Number",
    )
    fiscal_representative_community_vat_number = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Community VAT",
    )
    fiscal_representative_name = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Name",
    )
    fiscal_representative_incorporation = fields.Selection(
        copy=False,
        selection=[
            ('organization', "Organization"),
            ('self_employed', "Self Employed"),
            ('taxable_person', "Taxable Person"),
        ],
        index=True,
        readonly=True,
        string="Fiscal Representative Taxpayer Type",
    )
    fiscal_representative_vat_status = fields.Selection(
        copy=False,
        selection=[
            ('domestic', "Domestic"),
            ('private_person', "Private Person"),
            ('other', "Other"),
        ],
        index=True,
        readonly=True,
        string="Fiscal Representative VAT Status",
    )
    fiscal_representative_tax_number = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative Tax Number",
    )
    """ VAT GROUP
    fiscal_representative_vat_group = fields.Many2one(
        comodel_name='l10n_hu.l10n.hu.vat.group',
        copy=False,
        readonly=True,
        string="Fiscal Representative VAT Group",
    )
    fiscal_representative_vat_group_number = fields.Char(
        copy=False,
        readonly=True,
        string="Fiscal Representative VAT Group Number",
    )
    """
    # # invoiceHead invoiceDetail
    additional_invoice_data = fields.Text(
        copy=False,
        readonly=True,
        string="Additional Invoice Data",
    )
    advance_status = fields.Selection(
        compute='_compute_advance_status',
        selection=[
            ('none', "None"),
            ('issue', "Issue"),
            ('settlement', "Settlement"),
        ],
        store=True,
        string="Advance Status",
    )
    cash_accounting = fields.Boolean(
        copy=False,
        readonly=True,
        string="Cash Accounting",
    )
    currency_code = fields.Char(
        copy=False,
        readonly=True,
        string="Currency Code",
    )
    electronic_invoice_hash = fields.Char(
        copy=False,
        readonly=True,
        string="Hash",
    )
    exchange_rate = fields.Float(
        copy=False,
        readonly=True,
        string="Exchange Rate",
    )
    invoice_accounting_delivery_date = fields.Date(
        copy=False,
        readonly=True,
        string="Invoice Accounting Delivery Date",
    )
    invoice_appearance = fields.Selection(
        copy=False,
        readonly=True,
        selection=[
            ('paper', "Paper"),
            ('electronic', "Electronic"),
            ('edi', "EDI"),
            ('unknown', "Unknown"),
        ],
        string="Invoice Appearance",
    )
    invoice_delivery_date = fields.Date(
        copy=False,
        readonly=True,
        string="Invoice Delivery Date",
    )
    invoice_delivery_period_start = fields.Date(
        copy=False,
        readonly=True,
        string="Invoice Delivery Period Start",
    )
    invoice_delivery_period_end = fields.Date(
        copy=False,
        readonly=True,
        string="Invoice Delivery Period End",
    )
    invoice_direction = fields.Selection(
        copy=False,
        readonly=True,
        selection=[
            ('inbound', "Inbound"),
            ('outbound', "Outbound")
        ],
        string="Invoice Direction",
    )
    invoice_issue_date = fields.Date(
        copy=False,
        readonly=True,
        string="Invoice Issue Date",
    )
    invoice_number = fields.Char(
        copy=False,
        readonly=True,
        string="Invoice Number",
    )
    invoice_status = fields.Selection(
        copy=False,
        default='draft',
        selection=[
            ('draft', "Draft"),
            ('invoice', "Invoice"),
            ('external_invoice', "External invoice"),
            ('modified_invoice', "Modified invoice"),
            ('modification_invoice', "Modification invoice"),
            ('modification_in_progress', "Modification in progress"),
            ('cancelled_invoice', "Cancelled invoice"),
            ('cancellation_invoice', "Cancellation invoice")
        ],
        readonly=True,
        string="Invoice Status",
    )
    payment_date = fields.Date(
        copy=False,
        readonly=True,
        string="Payment Date",
    )
    payment_method = fields.Selection(
        copy=False,
        readonly=True,
        selection=[
            ('transfer', "Transfer"),
            ('cash', "Cash"),
            ('card', "Card"),
            ('voucher', "Voucher"),
            ('other', "Other"),
        ],
        string="Payment Method",
    )
    periodical_delivery = fields.Boolean(
        copy=False,
        default=False,
        readonly=True,
        string="Periodical Delivery",
    )
    self_billing = fields.Boolean(
        copy=False,
        readonly=True,
        string="Self Billing",
    )
    small_business = fields.Boolean(
        copy=False,
        readonly=True,
        string="Small Business",
    )
    # # invoiceSummary
    invoice_gross_amount = fields.Monetary(
        currency_field='currency',
        string="Invoice Gross Amount",
    )
    invoice_gross_amount_huf = fields.Monetary(
        currency_field='currency_huf',
        string="Invoice Gross Amount HUF",
    )
    invoice_gross_amount_huf_text_hu = fields.Text(
        compute='_compute_amount_huf_text_hu',
        string="Invoice Gross Amount HUF Text HU",
    )
    invoice_net_amount = fields.Monetary(
        currency_field='currency',
        string="Invoice Net Amount",
    )
    invoice_net_amount_huf = fields.Monetary(
        currency_field='currency_huf',
        string="Invoice Net Amount HUF",
    )
    invoice_net_amount_huf_text_hu = fields.Text(
        compute='_compute_amount_huf_text_hu',
        string="Invoice Net Amount HUF Text HU",
    )
    invoice_summary = fields.One2many(
        comodel_name='l10n.hu.invoice.summary',
        inverse_name='invoice',
        index=True,
        string="Invoice Summary",
    )
    invoice_vat_amount = fields.Monetary(
        currency_field='currency',
        string="Invoice VAT Amount",
    )
    invoice_vat_amount_huf = fields.Monetary(
        currency_field='currency_huf',
        string="Invoice VAT Amount HUF",
    )
    invoice_vat_amount_huf_text_hu = fields.Text(
        compute='_compute_amount_huf_text_hu',
        string="Invoice VAT Amount HUF Text HU",
    )

    # Compute and search fields, in the same order of field declarations
    @api.depends('invoice_line')
    def _compute_advance_status(self):
        for record in self:
            advance_status = 'none'
            if record.document_type \
                    and record.document_type.technical_name == 'invoice_advance':
                advance_status = 'issue'
            elif record.invoice_line:
                advance_lines = 0
                non_advance_lines = 0
                for line in record.invoice_line:
                    if line.advance_indicator:
                        advance_lines += 1
                    else:
                        non_advance_lines += 1
                if advance_lines > 0 and non_advance_lines == 0:
                    advance_status = 'issue'
                elif advance_lines > 0 and non_advance_lines > 0:
                    advance_status = 'settlement'
                else:
                    pass
            else:
                pass

            # Set value
            record.advance_status = advance_status

    @api.depends('invoice_log')
    def _compute_invoice_log_count(self):
        for record in self:
            record.invoice_log_count = self.env['l10n.hu.invoice.log'].search_count([
                ('invoice', '=', record.id)
            ])

    def _compute_amount_huf_text_hu(self):
        for record in self:
            # gross_huf_text_hu
            gross_huf_result = l10n_hu_amount_to_text.l10n_hu_amount_to_text(record.invoice_gross_amount_huf)
            gross_huf_text_hu = gross_huf_result.get('amount_text', "") + " forint"
            # gross_huf_text_hu = str(gross_huf_result.get('debug_list'))

            # net_huf_text_hu
            net_huf_result = l10n_hu_amount_to_text.l10n_hu_amount_to_text(record.invoice_net_amount_huf)
            net_huf_text_hu = net_huf_result.get('amount_text', "") + " forint"
            # net_huf_text_hu = str(net_huf_result.get('debug_list'))

            # vat_huf_text_hu
            vat_huf_result = l10n_hu_amount_to_text.l10n_hu_amount_to_text(record.invoice_vat_amount_huf)
            vat_huf_text_hu = vat_huf_result.get('amount_text', "") + " forint"
            # vat_huf_text_hu = str(vat_huf_result.get('debug_list'))

            # Set values
            record.invoice_gross_amount_huf_text_hu = gross_huf_text_hu
            record.invoice_net_amount_huf_text_hu = net_huf_text_hu
            record.invoice_vat_amount_huf_text_hu = vat_huf_text_hu

    def _compute_reference(self):
        for record in self:
            record.reference = "HUNINV-" + str(record.id)

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize result
        result = []

        # Iterate through self
        for record in self:
            # Set name
            if record.account_move:
                name = record.account_move.display_name
            else:
                name = "HUNINV-" + str(record.id)

            # Append to list
            result.append((record.id, name))

        # Return result
        return result

    def write(self, values):
        for record in self:
            # Cleanup values
            values = record.manage_write_values(values)

        # Super
        return super(L10nHuAccountInvoice, self).write(values)

    # Action methods
    def action_file_json(self):
        """ Get invoice as json """
        # Ensure one
        self.ensure_one()

        # Get values
        values = self.get_account_move_pull_values()

        # Write
        self.write(values)

        # Return result
        return

    def action_file_pdf(self):
        """ Get invoice as pdf """
        # Ensure one
        self.ensure_one()

        # Search
        if self.account_move and not self.file_pdf:
            # Print invoice
            self.account_move.action_invoice_print()

            # Assemble invoice_file_name
            invoice_file_name = self.invoice_number.replace("/", "") + ".pdf"

            # Get attachment
            attachment = self.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'account.move'),
                ('res_id', '=', self.account_move.id),
                ('name', '=', invoice_file_name),
            ], limit=1)
            # raise exceptions.UserError(str(attachment))

            if attachment:
                write_values = {
                    'file_pdf': attachment.datas
                }
                self.sudo().write(write_values)
            else:
                # Tuple is returned, we need only first item
                pdf = self.env.ref('account.account_invoices')._render_qweb_pdf(self.account_move.id)[0]
                pdf_encoded = base64.b64encode(pdf)
                write_values = {
                    'file_pdf': pdf_encoded
                }
                self.sudo().write(write_values)
        # Return result
        return

    def action_file_xml(self):
        """ Get invoice as xml """
        # Ensure one
        self.ensure_one()

        # Get values
        values = self.get_account_move_pull_values()

        # Write
        self.write(values)

        # Return result
        return

    def action_file_zip(self):
        """ Get invoice as zip """
        # Ensure one
        self.ensure_one()

        # Get values
        values = self.get_account_move_pull_values()

        # Write
        self.write(values)

        # Return result
        return

    def action_list_invoice_logs(self):
        """ List related logs """
        # Ensure one record in self
        self.ensure_one()

        # Assemble result
        result = {
            'name': _("Invoice Log"),
            'domain': [('invoice', '=', self.id)],
            'res_model': 'l10n.hu.invoice.log',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    def action_pull_from_account_move(self):
        """ Pull  data from account move """
        # Ensure one TODO copy wizard fails if ensure_one is active!!! Temporarily disabled!!!
        # self.ensure_one()

        # Do pull
        self.pull_from_account_move()

        # Return
        return

    def action_push_to_account_move(self):
        """ Push (create/update) record to account move """
        # Ensure one record in self
        self.ensure_one()

        # Checks
        if not self.account_move:
            raise exceptions.UserError(_("Account move not set!"))

        # Checks
        if self.technical_source == 'account_move' and self.account_move.move_type in ['out_invoice', 'out_refund']:
            raise exceptions.UserError(_("This invoice is not allowed to update the linked account move!"))

        # Do push
        self.push_to_account_move()

        # Return
        return

    def action_run_invoice_maintenance(self):
        """ Run invoice maintenance """
        # Ensure one record in self
        self.ensure_one()

        # Checks
        if not self.account_move:
            raise exceptions.UserError(_("Account move not set!"))

        # Do maintenance
        maintenance_result = self.run_invoice_maintenance({})
        # raise exceptions.UserError(str(maintenance_result))

        # Return
        return

    # Business methods
    @api.model
    def get_account_move_pull_values(self, account_move=None):
        """ Get data from an account move

        :param: account_move: an account move record

        :return: dictionary
        """
        # Set account_move
        if not account_move and self.account_move:
            account_move = self.account_move

        if not account_move:
            return

        # Initialize variables
        result = {}

        # Get customer_values
        customer_values = self.get_account_move_pull_values_customer(account_move)
        result.update(customer_values)

        # Get fiscal_representative_values
        fiscal_representative_values = self.get_account_move_pull_values_fiscal_representative(account_move)
        result.update(fiscal_representative_values)

        # Get invoice_detail_values
        invoice_detail_values = self.get_account_move_pull_values_invoice_detail(account_move)
        result.update(invoice_detail_values)

        # Get invoice_line_values
        # # This function creates/updates lines, does not return any value
        # # We pass on invoice_detail_values so that we can reuse what we already computed
        self.get_account_move_pull_values_invoice_line(account_move, invoice_detail_values)

        invoice_line_count = self.env['l10n_hu.invoice.line'].search_count([
            ('invoice', '=', self.id)
        ])

        # Set line count
        result.update({
            'invoice_line_count': invoice_line_count,
        })

        # Set invoice_summary
        # NOTE: this method executes the summary create/update
        self.get_account_move_pull_values_invoice_summary(account_move)

        # Get supplier_values
        supplier_values = self.get_account_move_pull_values_supplier(account_move)
        result.update(supplier_values)

        # Return result
        return result

    @api.model
    def get_account_move_pull_values_customer(self, account_move):
        """ Get customer values from account move

        :param account_move: an account move record

        :return: dictionary
        """
        # Initialize variables
        customer_address_building = ""
        customer_address_country_code = ""
        customer_address_country_id = False
        customer_address_country_name = ""
        customer_address_country_state_name = ""
        customer_address_country_state_code = ""
        customer_address_district = ""
        customer_address_door = ""
        customer_address_floor = ""
        customer_address_house_number = ""
        customer_address_lot_number = ""
        customer_address_public_place_name = ""
        customer_address_public_place_type = ""
        customer_address_postal_code = ""
        customer_address_settlement = ""
        customer_address_staircase = ""
        customer_address_street = ""
        customer_address_street2 = ""
        customer_address_type = ""
        error_text = ""

        # Set invoice_direction
        if account_move.move_type in ['in_invoice', 'in_refund']:
            invoice_direction = 'inbound'
        elif account_move.move_type in ['out_invoice', 'out_refund']:
            invoice_direction = 'outbound'
        else:
            invoice_direction = False

        # Customer
        if invoice_direction == 'inbound':
            customer = account_move.company_id.partner_id
            customer_name = account_move.company_id.partner_id.display_name
        elif invoice_direction == 'outbound':
            if account_move.partner_id.parent_id and account_move.partner_id.type == 'invoicing':
                customer = account_move.partner_id.parent_id
                customer_name = account_move.partner_id.parent_id.display_name
            else:
                customer = account_move.partner_id
                customer_name = account_move.partner_id.display_name
        else:
            return {}

        # Customer address
        if customer.country_id and customer.street:
            customer_address_type = 'simple'
            customer_address_country_id = customer.country_id.id
            customer_address_country_code = customer.country_id.code
            customer_address_country_name = customer.country_id.name
            customer_address_postal_code = customer.zip
            customer_address_settlement = customer.city
            customer_address_street = customer.street
            customer_address_street2 = customer.street2
        else:
            error_text += "\n" + _("Customer address is missing!")

        # Customer bank account
        if invoice_direction == 'inbound':
            # TODO review
            # customer_bank_account = account_move.l10n_hu_company_bank_account
            customer_bank_account = False
        elif invoice_direction == 'outbound':
            customer_bank_account = account_move.partner_bank_id
        else:
            customer_bank_account = False
        if customer_bank_account:
            customer_bank_account_number = customer_bank_account.acc_number
        else:
            customer_bank_account_number = ""

        # Customer fiscal position
        if invoice_direction == 'inbound':
            customer_fiscal_position = account_move.company_id.partner_id.property_account_position_id
        elif invoice_direction == 'outbound':
            customer_fiscal_position = account_move.partner_id.property_account_position_id
        else:
            customer_fiscal_position = False

        if customer_fiscal_position:
            customer_fiscal_position_id = customer_fiscal_position.id
            customer_fiscal_position_name = customer_fiscal_position.name
        else:
            customer_fiscal_position_id = False
            customer_fiscal_position_name = ""

        # Customer vat group TODO review
        """
        if customer.commercial_partner_id and customer.commercial_partner_id.l10n_hu_l10n_hu_vat_group:
            customer_tax_number = customer.commercial_partner_id.l10n_hu_l10n_hu_vat_group.name
            customer_vat_group_id = customer.commercial_partner_id.l10n_hu_l10n_hu_vat_group.id
            customer_vat_group_number = customer.commercial_partner_id.l10n_hu_l10n_hu_vat_group.name
            customer_vat_group_member_number = customer.commercial_partner_id.l10n_hu_l10n_hu_vat
        else:
            customer_tax_number = customer.commercial_partner_id.l10n_hu_l10n_hu_vat
            customer_vat_group_id = False
            customer_vat_group_number = ""
            customer_vat_group_member_number = ""
        """
        customer_tax_number = customer.commercial_partner_id.l10n_hu_vat

        # result
        result = {
            'customer': customer.id,
            'customer_address_building': customer_address_building,
            'customer_address_country': customer_address_country_id,
            'customer_address_country_state_name': customer_address_country_state_name,
            'customer_address_country_state_code': customer_address_country_state_code,
            'customer_address_country_name': customer_address_country_name,
            'customer_address_country_code': customer_address_country_code,
            'customer_address_district': customer_address_district,
            'customer_address_door': customer_address_door,
            'customer_address_floor': customer_address_floor,
            'customer_address_house_number': customer_address_house_number,
            'customer_address_lot_number': customer_address_lot_number,
            'customer_address_postal_code': customer_address_postal_code,
            'customer_address_public_place_name': customer_address_public_place_name,
            'customer_address_public_place_type': customer_address_public_place_type,
            'customer_address_settlement': customer_address_settlement,
            'customer_address_staircase': customer_address_staircase,
            'customer_address_street': customer_address_street,
            'customer_address_street2': customer_address_street2,
            'customer_address_type': customer_address_type,
            'customer_bank_account': customer_bank_account,
            'customer_bank_account_number': customer_bank_account_number,
            'customer_community_vat_number': customer.commercial_partner_id.vat,
            'customer_fiscal_position': customer_fiscal_position_id,
            'customer_fiscal_position_name': customer_fiscal_position_name,
            'customer_incorporation': customer.commercial_partner_id.l10n_hu_incorporation,
            'customer_name': customer_name,
            'customer_tax_number': customer_tax_number,
            'customer_third_state_tax_id': customer.commercial_partner_id.vat,
            'customer_vat_status': customer.commercial_partner_id.l10n_hu_vat_status,
            # 'customer_vat_group': customer_vat_group_id,
            # 'customer_vat_group_number': customer_vat_group_number,
            # 'customer_vat_group_member_number': customer_vat_group_member_number,
        }

        # Return result
        return result

    @api.model
    def get_account_move_pull_values_fiscal_representative(self, account_move):
        """ Get fiscal representative values

        NOTE:
        - The result somewhat corresponds to the fiscalRepresentativeInfo element of the NAV schema

        :return: dictionary
        """
        # Return result if not set
        if not account_move.l10n_hu_fiscal_representative:
            return {}

        # Initialize variables
        fiscal_representative_address_building = ""
        fiscal_representative_address_country_code = ""
        fiscal_representative_address_country_id = False
        fiscal_representative_address_country_name = ""
        fiscal_representative_address_country_state_name = ""
        fiscal_representative_address_country_state_code = ""
        fiscal_representative_address_district = ""
        fiscal_representative_address_door = ""
        fiscal_representative_address_floor = ""
        fiscal_representative_address_house_number = ""
        fiscal_representative_address_lot_number = ""
        fiscal_representative_address_public_place_name = ""
        fiscal_representative_address_public_place_type = ""
        fiscal_representative_address_postal_code = ""
        fiscal_representative_address_settlement = ""
        fiscal_representative_address_staircase = ""
        fiscal_representative_address_street = ""
        fiscal_representative_address_street2 = ""
        fiscal_representative_address_type = ""
        error_text = ""

        # Set invoice_direction
        if account_move.move_type in ['in_invoice', 'in_refund']:
            invoice_direction = 'inbound'
        elif account_move.move_type in ['out_invoice', 'out_refund']:
            invoice_direction = 'outbound'
        else:
            invoice_direction = False

        # fiscal_representative
        if invoice_direction in ['inbound', 'outbound']:
            if account_move.l10n_hu_fiscal_representative.parent_id:
                fiscal_representative = account_move.l10n_hu_fiscal_representative.parent_id
                fiscal_representative_name = account_move.l10n_hu_fiscal_representative.parent_id.display_name
            else:
                fiscal_representative = account_move.l10n_hu_fiscal_representative
                fiscal_representative_name = account_move.l10n_hu_fiscal_representative.display_name
        else:
            return {}

        # fiscal_representative address
        if fiscal_representative.country_id and fiscal_representative.street:
            fiscal_representative_address_type = 'simple'
            fiscal_representative_address_country_id = fiscal_representative.country_id.id
            fiscal_representative_address_country_code = fiscal_representative.country_id.code
            fiscal_representative_address_country_name = fiscal_representative.country_id.name
            fiscal_representative_address_postal_code = fiscal_representative.zip
            fiscal_representative_address_settlement = fiscal_representative.city
            fiscal_representative_address_street = fiscal_representative.street
            fiscal_representative_address_street2 = fiscal_representative.street2
        else:
            error_text += "\n" + _("Fiscal_representative address is missing!")

        # Fiscal representative bank account
        if invoice_direction == 'inbound':
            fiscal_representative_bank_account = account_move.l10n_hu_company_bank_account
        elif invoice_direction == 'outbound':
            fiscal_representative_bank_account = account_move.partner_bank_id
        else:
            fiscal_representative_bank_account = False

        if fiscal_representative_bank_account:
            fiscal_representative_bank_account_number = fiscal_representative_bank_account.acc_number
        else:
            fiscal_representative_bank_account_number = ""

        # Fiscal representative vat group TODO
        """
        if fiscal_representative.l10n_hu_vat_group:
            fiscal_representative_vat_group_id = fiscal_representative.l10n_hu_vat_group.id
            fiscal_representative_vat_group_number = fiscal_representative.l10n_hu_vat_group.name
        else:
            fiscal_representative_vat_group_id = False
            fiscal_representative_vat_group_number = ""
        """

        # Assemble result
        result = {
            'fiscal_representative': fiscal_representative.id,
            'fiscal_representative_address_building': fiscal_representative_address_building,
            'fiscal_representative_address_country': fiscal_representative_address_country_id,
            'fiscal_representative_address_country_state_name': fiscal_representative_address_country_state_name,
            'fiscal_representative_address_country_state_code': fiscal_representative_address_country_state_code,
            'fiscal_representative_address_country_name': fiscal_representative_address_country_name,
            'fiscal_representative_address_country_code': fiscal_representative_address_country_code,
            'fiscal_representative_address_district': fiscal_representative_address_district,
            'fiscal_representative_address_door': fiscal_representative_address_door,
            'fiscal_representative_address_floor': fiscal_representative_address_floor,
            'fiscal_representative_address_house_number': fiscal_representative_address_house_number,
            'fiscal_representative_address_lot_number': fiscal_representative_address_lot_number,
            'fiscal_representative_address_postal_code': fiscal_representative_address_postal_code,
            'fiscal_representative_address_public_place_name': fiscal_representative_address_public_place_name,
            'fiscal_representative_address_public_place_type': fiscal_representative_address_public_place_type,
            'fiscal_representative_address_settlement': fiscal_representative_address_settlement,
            'fiscal_representative_address_staircase': fiscal_representative_address_staircase,
            'fiscal_representative_address_street': fiscal_representative_address_street,
            'fiscal_representative_address_street2': fiscal_representative_address_street2,
            'fiscal_representative_address_type': fiscal_representative_address_type,
            'fiscal_representative_bank_account': fiscal_representative_bank_account,
            'fiscal_representative_bank_account_number': fiscal_representative_bank_account_number,
            'fiscal_representative_community_vat_number': fiscal_representative.vat,
            'fiscal_representative_incorporation': fiscal_representative.l10n_hu_incorporation,
            'fiscal_representative_name': fiscal_representative_name,
            'fiscal_representative_tax_number': fiscal_representative.l10n_hu_l10n_hu_vat,
            'fiscal_representative_vat_status': fiscal_representative.l10n_hu_vat_status,
            # 'fiscal_representative_vat_group': fiscal_representative_vat_group_id,
            # 'fiscal_representative_vat_group_number': fiscal_representative_vat_group_number,
        }

        # Return result
        return result

    @api.model
    def get_account_move_pull_values_invoice_detail(self, account_move):
        """ Get values from account move to populate invoice header information

        This somewhat corresponds to NAV schema's invoiceDetail element

        :return dictionary
        """
        # Get invoice_category based on l10n_hu_document_type_code
        # TODO rewrite to use technical_name
        if account_move.l10n_hu_document_type_code in ['1', '3', '4', '6']:
            invoice_category = 'normal'
        elif account_move.l10n_hu_document_type_code in ['2']:
            invoice_category = 'simplified'
        elif account_move.l10n_hu_document_type_code in ['5']:
            invoice_category = 'aggregate'
        else:
            invoice_category = False

        # Get invoice_operation based on l10n_hu_document_type_code
        # TODO rewrite to use technical_name
        if account_move.l10n_hu_document_type_code in ['1', '2', '5', '6']:
            invoice_operation = 'create'
        elif account_move.l10n_hu_document_type_code in ['3']:
            invoice_operation = 'modify'
        elif account_move.l10n_hu_document_type_code in ['4']:
            invoice_operation = 'storno'
        else:
            invoice_operation = False

        # Amount sign
        if invoice_operation == 'modify'\
                and account_move.move_type in ['out_invoice', 'out_receipt']:
            amount_sign = 1
        elif invoice_operation == 'modify' \
                and account_move.move_type in ['out_refund']:
            amount_sign = -1
        elif invoice_operation == 'storno':
            amount_sign = -1
        elif account_move.move_type == 'out_refund':
            amount_sign = -1
        else:
            amount_sign = 1

        # consider rounding lines (not base for tax!)
        rounding_net_amount = 0
        rounding_gross_amount = 0

        for line in account_move.invoice_line_ids:
            is_processable_line = line.l10n_hu_is_processable_invoice_line()
            is_rounding_line = line.l10n_hu_is_invoice_rounding_line()

            # NOTE: if processable, it will already be taken into account, we do not need to subtract here
            if is_rounding_line and not is_processable_line:
                rounding_net_amount += line.price_subtotal
                rounding_gross_amount += line.price_total

        # Set invoice amounts
        rounding_tax_amount = rounding_gross_amount - rounding_net_amount
        invoice_net_amount = (account_move.amount_untaxed - rounding_net_amount) * amount_sign
        invoice_vat_amount = (account_move.amount_tax - rounding_tax_amount) * amount_sign
        invoice_gross_amount = (account_move.amount_total - rounding_gross_amount) * amount_sign

        # Set currency rate and exchange rate
        currency_rate_huf_id = False
        currency_rate_huf_amount = False
        currency_rate_huf_date = False
        currency_huf = self.env['res.currency'].search([
            ('name', '=', 'HUF'),
            '|',
            ('active', '=', True),
            ('active', '=', False),
        ])

        if currency_huf:
            currency_huf_id = currency_huf.id
        else:
            currency_huf_id = False

        # If company currency and invoice currency are both HUF
        if currency_huf \
                and currency_huf == account_move.company_id.currency_id \
                and account_move.currency_id == currency_huf:
            currency_rate_huf_amount = 1.0
            exchange_rate = currency_rate_huf_amount

            # Set invoice HUF amounts
            invoice_net_amount_huf = invoice_net_amount
            invoice_vat_amount_huf = invoice_vat_amount
            invoice_gross_amount_huf = invoice_gross_amount
        # If company currency is HUF and invoice currency is not HUF
        elif currency_huf \
                and currency_huf == account_move.company_id.currency_id \
                and self.currency != currency_huf:
            # We have a rate set on the invoice
            try:
                currency_rate_huf_id = account_move.l10n_hu_currency_rate.id
                # currency_rate_huf_amount = round(1 / account_move.l10n_hu_currency_rate.rate, 2)
                currency_rate_huf_amount = 1 / account_move.l10n_hu_currency_rate.rate
                currency_rate_huf_date = account_move.l10n_hu_currency_rate.name
            # Else get a rate (failsafe)
            except:
                currency_rate_huf = self.env['res.currency.rate'].sudo().search([
                    ('company_id', '=', account_move.company_id.id),
                    ('currency_id', '=', currency_huf.id),
                    ('name', '<=', account_move.invoice_date),
                ], limit=1)
                try:
                    currency_rate_huf_id = currency_rate_huf.id
                    # currency_rate_huf_amount = round(1 / currency_rate_huf, 2)
                    currency_rate_huf_amount = 1 / currency_rate_huf
                    currency_rate_huf_date = currency_rate_huf.name
                except:
                    currency_rate_huf_id = False
                    currency_rate_huf_amount = 0.0
                    currency_rate_huf_date = False

            try:
                # Lets round here to 2 decimals
                exchange_rate = round(currency_rate_huf_amount, 2)
                # exchange_rate = currency_rate_huf_amount
            except:
                exchange_rate = 1.0

            # Set invoice HUF amounts
            invoice_net_amount_huf = invoice_net_amount * exchange_rate
            invoice_vat_amount_huf = invoice_vat_amount * exchange_rate
            invoice_gross_amount_huf = invoice_gross_amount * exchange_rate
        # If company currency is not HUF and invoice currency is HUF
        elif currency_huf \
                and currency_huf != account_move.company_id.currency_id \
                and account_move.currency_id == currency_huf:
            currency_rate_huf = self.env['res.currency.rate'].sudo().search([
                ('company_id', '=', account_move.company_id.id),
                ('currency_id', '=', currency_huf.id),
                ('name', '<=', account_move.invoice_date),
            ], limit=1)

            # NOTE: currency_rate_huf and self.currency_rate should be the same in this case...
            if currency_rate_huf and self.currency_rate:
                amount_for_huf = self.currency_rate.rate
                currency_rate_huf_id = currency_rate_huf.id
                currency_rate_huf_amount = currency_huf.round(amount_for_huf)
                currency_rate_huf_date = currency_rate_huf.name
                # NOTE: nothing to exchange in this scenario, the invoice is in HUF!
                exchange_rate = 1.0

                # Set invoice HUF amounts
                invoice_net_amount_huf = invoice_net_amount * exchange_rate
                invoice_vat_amount_huf = invoice_vat_amount * exchange_rate
                invoice_gross_amount_huf = invoice_gross_amount * exchange_rate
            else:
                exchange_rate = 1.0

                # Set invoice HUF amounts
                invoice_net_amount_huf = invoice_net_amount * exchange_rate
                invoice_vat_amount_huf = invoice_vat_amount * exchange_rate
                invoice_gross_amount_huf = invoice_gross_amount * exchange_rate
        # If company currency is not HUF and invoice currency is not the same as company currency
        elif currency_huf \
                and currency_huf != account_move.company_id.currency_id \
                and account_move.currency_id != account_move.company_id.currency_id:
            currency_rate_huf = self.env['res.currency.rate'].sudo().search([
                ('company_id', '=', account_move.company_id.id),
                ('currency_id', '=', currency_huf.id),
                ('name', '<=', account_move.invoice_date),
            ], limit=1)

            # Example: company EUR, account move USD
            # currency_rate_huf = 350 HUF/EUR
            # currency_rate = 1,25 USD/EUR
            if currency_rate_huf and self.currency_rate:
                amount_for_huf = currency_rate_huf.rate
                currency_rate_huf_id = currency_rate_huf.id
                currency_rate_huf_amount = currency_huf.round(amount_for_huf)
                currency_rate_huf_date = currency_rate_huf.name
                exchange_rate = amount_for_huf

                # Set invoice HUF amounts
                invoice_net_amount_huf = invoice_net_amount * exchange_rate
                invoice_vat_amount_huf = invoice_vat_amount * exchange_rate
                invoice_gross_amount_huf = invoice_gross_amount * exchange_rate
            else:
                exchange_rate = 1.0

                # Set invoice HUF amounts
                invoice_net_amount_huf = invoice_net_amount * exchange_rate
                invoice_vat_amount_huf = invoice_vat_amount * exchange_rate
                invoice_gross_amount_huf = invoice_gross_amount * exchange_rate
        else:
            exchange_rate = 1.0

            # Set invoice HUF amounts
            invoice_net_amount_huf = invoice_net_amount * exchange_rate
            invoice_vat_amount_huf = invoice_vat_amount * exchange_rate
            invoice_gross_amount_huf = invoice_gross_amount * exchange_rate

        # Set invoice_appearance - TODO: we use 'paper' as default for now
        invoice_appearance = 'paper'

        # Set invoice_direction
        if account_move.move_type in ['in_invoice', 'in_refund']:
            invoice_direction = 'inbound'
        elif account_move.move_type in ['out_invoice', 'out_refund']:
            invoice_direction = 'outbound'
        else:
            invoice_direction = False

        # Set invoice number
        if invoice_direction == 'inbound':
            invoice_number = account_move.ref
        elif invoice_direction == 'outbound':
            invoice_number = account_move.name
        else:
            invoice_number = False

        # Fiscal position
        if account_move.fiscal_position_id:
            fiscal_position_id = account_move.fiscal_position_id.id
            fiscal_position_name = account_move.fiscal_position_id.name
        else:
            fiscal_position_id = False
            fiscal_position_name = ""

        # Set payment_method
        if account_move.invoice_payment_term_id \
                and account_move.invoice_payment_term_id.l10n_hu_payment_method \
                and account_move.invoice_payment_term_id.l10n_hu_payment_method.l10n_hu_method:
            payment_method = account_move.invoice_payment_term_id.l10n_hu_payment_method.l10n_hu_method
        elif account_move.l10n_hu_invoice_payment_method \
                and account_move.l10n_hu_invoice_payment_method.l10n_hu_method:
            payment_method = account_move.l10n_hu_invoice_payment_method.l10n_hu_method
        elif account_move.journal_id \
                and account_move.journal_id.l10n_hu_invoice_payment_method_default \
                and account_move.journal_id.l10n_hu_invoice_payment_method_default.l10n_hu_method:
            payment_method = account_move.journal_id.l10n_hu_invoice_payment_method_default.l10n_hu_method
        else:
            payment_method = ""

        # result
        result = {
            'account_journal': account_move.journal_id.id,
            'company': account_move.company_id.id,
            'company_currency': account_move.company_id.currency_id.id,
            'company_currency_name': account_move.company_id.currency_id.name,
            'currency': account_move.currency_id.id,
            'currency_huf': currency_huf_id,
            'currency_code': account_move.currency_id.name,
            'currency_symbol': account_move.currency_id.symbol,
            'currency_rate': account_move.l10n_hu_currency_rate.id or False,
            'currency_rate_amount': account_move.l10n_hu_currency_rate_amount or 1,
            'currency_rate_date': account_move.l10n_hu_currency_rate.name or False,
            'currency_rate_huf': currency_rate_huf_id or False,
            'currency_rate_huf_amount': currency_rate_huf_amount or False,
            'currency_rate_huf_date': currency_rate_huf_date or False,
            'document_type': account_move.l10n_hu_document_type.id,
            'document_type_name': account_move.l10n_hu_document_type.name,
            'eu_oss_eligible': account_move.l10n_hu_eu_oss_eligible,
            'eu_oss_enabled': account_move.l10n_hu_eu_oss_enabled,
            'exchange_rate': exchange_rate,
            'fiscal_position': fiscal_position_id,
            'fiscal_position_name': fiscal_position_name,
            'invoice_appearance': invoice_appearance,
            'invoice_category': invoice_category,
            'invoice_delivery_date': account_move.l10n_hu_invoice_delivery_date,
            'invoice_delivery_period_end': account_move.l10n_hu_invoice_delivery_period_end,
            'invoice_delivery_period_start': account_move.l10n_hu_invoice_delivery_period_start,
            'invoice_direction': invoice_direction,
            'invoice_gross_amount': invoice_gross_amount,
            'invoice_gross_amount_huf': invoice_gross_amount_huf,
            'invoice_issue_date': account_move.invoice_date,
            'invoice_net_amount': invoice_net_amount,
            'invoice_net_amount_huf': invoice_net_amount_huf,
            'invoice_number': invoice_number,
            'invoice_operation': invoice_operation,
            'invoice_vat_amount': invoice_vat_amount,
            'invoice_vat_amount_huf': invoice_vat_amount_huf,
            'invoice_type': account_move.l10n_hu_document_type_code,
            'payment_date': account_move.invoice_date_due,
            'payment_method': payment_method,
            'payment_term': account_move.invoice_payment_term_id.id,
            'periodical_delivery': account_move.l10n_hu_invoice_periodical_delivery,
            'technical_source': 'account_move',
            'technical_type': account_move.move_type,
        }

        if account_move.l10n_hu_original_account_move:
            original_invoice = account_move.l10n_hu_original_account_move.l10n_hu_invoice
            original_invoice_id = original_invoice.id
            original_invoice_number = original_invoice.invoice_number
        elif account_move.l10n_hu_original_invoice_number:
            original_invoice_id = False
            original_invoice_number = account_move.l10n_hu_original_invoice_number
        else:
            original_invoice_id = False
            original_invoice_number = False

        result.update({
            'original_invoice': original_invoice_id,
            'original_invoice_number': original_invoice_number,
        })

        # Compute modification_index
        if original_invoice_number and invoice_operation in ['modify', 'storno']:
            previous_invoice_count = self.env['l10n.hu.invoice'].sudo().search_count([
                ('id', '!=', self.id),
                ('original_invoice_number', '=', original_invoice_number)
            ])
            modification_index = previous_invoice_count + 1
        else:
            modification_index = False

        result.update({
            'modification_index': modification_index,
        })

        # Compute modify_without_master
        if not original_invoice_number and invoice_operation == 'modify':
            modify_without_master = True
        else:
            modify_without_master = False

        result.update({
            'modify_without_master': modify_without_master,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result

    @api.model
    def get_account_move_pull_values_invoice_line(self, account_move, invoice_detail_values):
        """ Get values from account move to populate invoice line information

        This somewhat corresponds to NAV schema's invoiceLine element

        About line_index and line_number_next:
        1) if invoice_operation is 'create' than it starts at 1 and will be used for line numbering
        2) if invoice_operation is 'modify' or 'storno' than it starts at highest line number in the chain
            NOTE: INVALID_LINE_OPERATION blocking error was introduced in NAV API 3.21, after this change:
                    - line_operation can only be 'create'
                    - line numbering must be continuous among all modification/storno invoices

        :param account_move: an account move record

        :param invoice_detail_values: a dictionary of already computed values describing the invoice

        :return: nothing, corresponding records are created/updated in the background
        """
        # raise exceptions.UserError(str(account_move) + " --- " + str(invoice_detail_values))
        # Initialize variables
        managed_invoice_line_ids = []

        # original_invoice
        if self.original_invoice:
            original_invoice = self.original_invoice
        elif account_move.l10n_hu_original_account_move.l10n_hu_invoice:
            original_invoice = account_move.l10n_hu_original_account_move.l10n_hu_invoice
        elif invoice_detail_values.get('original_invoice'):
            original_invoice = self.env['l10n.hu.invoice'].sudo().search([
                ('id', '=', invoice_detail_values['original_invoice'])
            ], limit=1)
        else:
            original_invoice = False

        # invoice_operation
        if self.invoice_operation:
            invoice_operation = self.invoice_operation
        elif invoice_detail_values.get('invoice_operation'):
            invoice_operation = invoice_detail_values['invoice_operation']
        else:
            invoice_operation = 'unknown'

        # line_number
        line_number = 1

        # line_number_reference
        if original_invoice and invoice_operation in ['modify', 'storno']:
            modification_index = account_move.l10n_hu_invoice.modification_index
            highest_original_invoice_line = self.env['l10n.hu.invoice.line'].sudo().search([
                ('account_move.id', '!=', account_move.id),
                ('account_move.state', '=', 'posted'),
                ('account_move.l10n_hu_invoice.modification_index', '<', modification_index),
                '|',
                ('invoice', '=', original_invoice.id),
                ('original_invoice', '=', original_invoice.id),
            ], limit=1, order='line_number desc')
            if highest_original_invoice_line:
                line_number_reference = highest_original_invoice_line.line_number + 1
            else:
                # for debugging
                line_number_reference = 666
        else:
            # for debugging
            line_number_reference = 0
        # raise exceptions.UserError(str(line_number_reference_next))

        # Iterate lines
        for line in account_move.invoice_line_ids:
            # is_processable_line
            is_processable_line = line.l10n_hu_is_processable_invoice_line()

            # Process line
            if is_processable_line:
                # manage_values
                manage_values = {
                    'account_move_line': line,
                    'invoice_operation': invoice_operation,
                    'line_number': line_number,
                    'line_number_reference': line_number_reference,
                    'original_account_move_line': line.l10n_hu_original_account_move_line,
                    'original_invoice': original_invoice,
                }

                # Check if we already have a linked invoice line
                existing_line = self.env['l10n.hu.invoice.line'].search([
                    ('account_move_line', '=', line.id),
                    ('invoice', '=', self.id)
                ], limit=1)

                if existing_line:
                    # update manage_values
                    manage_values.update({
                        'crud': 'update',
                        'invoice': self,
                    })
                    # raise exceptions.UserError("existing_line" + str(manage_values))

                    # Get write_values
                    write_values = existing_line.get_account_move_line_values(manage_values)
                    # raise exceptions.UserError(str(write_values))

                    # line_number
                    if write_values.get('line_number') == line_number:
                        line_number += 1

                    # line_number_reference
                    if write_values.get('line_number_reference') == line_number_reference:
                        line_number_reference += 1

                    # analytic_tag
                    # TODO: we have analytic plan now
                    """
                    if line.analytic_tag_ids:
                        tag_ids = []
                        for tag in line.analytic_tag_ids:
                            tag_ids.append(tag.id)
                        write_values.update({
                            'analytic_tag': [(6, False, tag_ids)],
                        })
                    else:
                        write_values.update({
                            'analytic_tag': False,
                        })
                    """
                    # Write
                    # raise exceptions.UserError(str(write_values))
                    existing_line.write(write_values)

                    # Append to list
                    managed_invoice_line_ids.append(existing_line.id)
                else:
                    # update manage_values
                    manage_values.update({
                        'crud': 'create',
                        'invoice': self,
                    })
                    # raise exceptions.UserError("no existing_line" + str(manage_values))

                    # Get create_values
                    invoice_line_object = self.env['l10n.hu.invoice.line']
                    create_values = invoice_line_object.get_account_move_line_values(manage_values)

                    # line_number
                    if create_values.get('line_number') == line_number:
                        line_number += 1

                    # line_number_reference_next
                    if create_values.get('line_number_reference') == line_number_reference:
                        line_number_reference += 1

                    # analytic_tag
                    # TODO: we have analytic plan now
                    """
                    if line.analytic_tag_ids:
                        create_values.update({
                            'analytic_tag': [(4, x.id, False) for x in line.analytic_tag_ids],
                        })
                    """

                    # Create
                    new_line = self.env['l10n.hu.invoice.line'].create(create_values)

                    # Append to list
                    managed_invoice_line_ids.append(new_line.id)
            else:
                pass

        # clean up
        unnecessary_lines = self.env['l10n.hu.invoice.line'].sudo().search([
            ('id', 'not in', managed_invoice_line_ids),
            ('invoice', '=', self.id)
        ])
        for unnecessary_line in unnecessary_lines:
            unnecessary_line.sudo().unlink()

        # Return result
        return

    @api.model
    def get_account_move_pull_values_invoice_summary(self, account_move):
        """ Get values from account move to populate invoice summary information

        This somewhat corresponds to NAV schema's summaryByVatRate element

        We have two problems:
        1) Odoo is NOT creating account.move.line for 0% taxes.
            To manage these, we need to iterate invoice lines and assemble 0% tax dictionaries ourselves
        2) Odoo is NOT creating account.move.line for taxes with 0 amount
            A case is when we have a 0 total amount invoice because of deducting advance payments
            To manage these we need to assemble tax dictionaries ourselves

        :param account_move: an account move record

        :return: nothing, corresponding records are created/updated in the background
        """
        # Initialize variables
        created_summaries = []
        updated_summaries = []
        deleted_summaries = []
        invoice_taxes = []
        invoice_taxes_0_percent = []
        account_move_taxes = []
        summary_taxes = []

        # Delete all summaries, better to start from scratch
        self.env['l10n.hu.invoice.summary'].search([
            ('invoice', '=', self.id)
        ]).sudo().unlink()

        # Manage accounting lines (not invoice lines, this covers all non-0% and non-0 total amount taxes)
        for account_move_line in account_move.line_ids:
            # is_processable_summary
            is_processable_summary = account_move_line.l10n_hu_is_processable_invoice_summary()

            # Process
            if is_processable_summary \
                    and account_move_line.tax_group_id \
                    and account_move_line.tax_line_id \
                    and account_move_line.tax_line_id.l10n_hu_vat_enabled:
                # Check if we already have a linked invoice summary
                existing_summary = self.env['l10n.hu.invoice.summary'].search([
                    ('account_move_line', '=', account_move_line.id),
                    ('invoice', '=', self.id)
                ], limit=1)

                if existing_summary:
                    # Update summary
                    summary_parameters = {
                        'account_move_line': account_move_line,
                        'invoice': self,
                        'non_zero_rate': True,
                    }
                    summary_result = existing_summary.get_values_from_account_move_line(summary_parameters)
                    if len(summary_result['error_list']) == 0:
                        existing_summary.write(summary_result['crud_values'])

                        # Append to list
                        updated_summaries.append(existing_summary)

                    # Append to list
                    if existing_summary.account_tax not in account_move_taxes:
                        account_move_taxes.append(existing_summary.account_tax)
                    if existing_summary.account_tax not in summary_taxes:
                        summary_taxes.append(existing_summary.account_tax)
                else:
                    # Create summary
                    summary_parameters = {
                        'account_move_line': account_move_line,
                        'invoice': self,
                        'non_zero_rate': True,
                    }
                    summary_class = self.env['l10n.hu.invoice.summary']
                    summary_result = summary_class.get_values_from_account_move_line(summary_parameters)
                    if len(summary_result['error_list']) == 0:
                        new_summary = self.env['l10n.hu.invoice.summary'].create(summary_result['crud_values'])

                        # Append to list
                        created_summaries.append(new_summary)
                        if new_summary.account_tax not in account_move_taxes:
                            account_move_taxes.append(new_summary.account_tax)
                        if new_summary.account_tax not in summary_taxes:
                            summary_taxes.append(new_summary.account_tax)
            else:
                pass

        # Now manage 0% and 0 total amount taxes by iterating invoice lines
        invoice_lines_with_zero_percent_vat = []
        for invoice_line in account_move.invoice_line_ids:
            for tax in invoice_line.tax_ids:
                # Collect all invoice taxes
                if tax not in invoice_taxes:
                    invoice_taxes.append(tax)

                # Collect 0% invoice lines and taxes too
                if tax.l10n_hu_vat_enabled and tax.l10n_hu_vat_percentage == 0.0:
                    invoice_taxes_0_percent.append(tax)
                    invoice_lines_with_zero_percent_vat.append(invoice_line)
                    break
                else:
                    pass

        # Now iterate 0% tax lines
        for account_move_line in invoice_lines_with_zero_percent_vat:
            # is_processable_summary
            is_processable_summary = account_move_line.l10n_hu_is_processable_invoice_summary()

            # iterate taxes
            if is_processable_summary:
                for tax in account_move_line.tax_ids:
                    # Check if we already have a invoice.summary
                    existing_summary = self.env['l10n.hu.invoice.summary'].search([
                        ('account_tax', '=', tax.id),
                        ('invoice', '=', self.id)
                    ], limit=1)

                    if existing_summary:
                        # Update
                        summary_parameters = {
                            'account_move_line': account_move_line,
                            'invoice': self,
                            'non_zero_rate': False,
                        }
                        summary_result = existing_summary.get_values_from_account_move_line(summary_parameters)
                        if len(summary_result['error_list']) == 0:
                            # update values
                            vat_rate_gross_amount = existing_summary.vat_rate_gross_amount
                            vat_rate_gross_amount += summary_result['crud_values']['vat_rate_gross_amount']
                            vat_rate_gross_amount_huf = existing_summary.vat_rate_gross_amount_huf
                            vat_rate_gross_amount_huf += summary_result['crud_values']['vat_rate_gross_amount_huf']
                            vat_rate_net_amount = existing_summary.vat_rate_net_amount
                            vat_rate_net_amount += summary_result['crud_values']['vat_rate_net_amount']
                            vat_rate_net_amount_huf = existing_summary.vat_rate_net_amount_huf
                            vat_rate_net_amount_huf += summary_result['crud_values']['vat_rate_net_amount_huf']

                            # write_values
                            write_values = {
                                'vat_rate_gross_amount': vat_rate_gross_amount,
                                'vat_rate_gross_amount_huf': vat_rate_gross_amount_huf,
                                'vat_rate_net_amount': vat_rate_net_amount,
                                'vat_rate_net_amount_huf': vat_rate_net_amount_huf,
                            }

                            # Write
                            existing_summary.write(write_values)

                            # Append to list
                            updated_summaries.append(existing_summary)
                            if existing_summary.account_tax not in summary_taxes:
                                summary_taxes.append(existing_summary.account_tax)
                    else:
                        # Create
                        summary_parameters = {
                            'account_move_line': account_move_line,
                            'invoice': self,
                            'non_zero_rate': False,
                        }
                        summary_class = self.env['l10n.hu.invoice.summary']
                        summary_result = summary_class.get_values_from_account_move_line(summary_parameters)
                        if len(summary_result['error_list']) == 0:
                            new_summary = summary_class.create(summary_result['crud_values'])

                            # Append to list
                            created_summaries.append(new_summary)
                            if new_summary.account_tax not in summary_taxes:
                                summary_taxes.append(new_summary.account_tax)

        # Now manage 0 total amount taxes
        not_yet_managed_taxes = list(set(invoice_taxes) - set(summary_taxes))
        for not_yet_managed_tax in not_yet_managed_taxes:
            tax_lines_total_amount = 0
            for account_move_line in account_move.invoice_line_ids:
                # is_processable_summary
                is_processable_summary = account_move_line.l10n_hu_is_processable_invoice_summary()

                # skip not processable (eg: display sections)
                if is_processable_summary:
                    if not_yet_managed_tax in account_move_line.tax_ids:
                        tax_lines_total_amount += account_move_line.price_total

                    # Check if we already have a invoice.summary
                    existing_summary = self.env['l10n.hu.invoice.summary'].search([
                        ('account_tax', '=', not_yet_managed_tax.id),
                        ('invoice', '=', self.id)
                    ], limit=1)

                    if existing_summary:
                        # Update
                        summary_parameters = {
                            'account_move_line': account_move_line,
                            'invoice': self,
                            'non_zero_rate': True,
                        }
                        summary_result = existing_summary.get_values_from_account_move_line(summary_parameters)
                        if len(summary_result['error_list']) == 0:
                            # update values
                            vat_rate_gross_amount = existing_summary.vat_rate_gross_amount
                            vat_rate_gross_amount += summary_result['crud_values']['vat_rate_gross_amount']
                            vat_rate_gross_amount_huf = existing_summary.vat_rate_gross_amount_huf
                            vat_rate_gross_amount_huf += summary_result['crud_values']['vat_rate_gross_amount_huf']
                            vat_rate_net_amount = existing_summary.vat_rate_net_amount
                            vat_rate_net_amount += summary_result['crud_values']['vat_rate_net_amount']
                            vat_rate_net_amount_huf = existing_summary.vat_rate_net_amount_huf
                            vat_rate_net_amount_huf += summary_result['crud_values']['vat_rate_net_amount_huf']
                            vat_rate_vat_amount = existing_summary.vat_rate_vat_amount
                            vat_rate_vat_amount += summary_result['crud_values']['vat_rate_vat_amount']
                            vat_rate_vat_amount_huf = existing_summary.vat_rate_vat_amount_huf
                            vat_rate_vat_amount_huf += summary_result['crud_values']['vat_rate_vat_amount_huf']

                            # write_values
                            write_values = {
                                'vat_rate_gross_amount': vat_rate_gross_amount,
                                'vat_rate_gross_amount_huf': vat_rate_gross_amount_huf,
                                'vat_rate_net_amount': vat_rate_net_amount,
                                'vat_rate_net_amount_huf': vat_rate_net_amount_huf,
                                'vat_rate_vat_amount': vat_rate_vat_amount,
                                'vat_rate_vat_amount_huf': vat_rate_vat_amount_huf,
                            }

                            # Write
                            existing_summary.write(write_values)

                            # Append to list
                            updated_summaries.append(existing_summary)
                        if existing_summary.account_tax not in summary_taxes:
                            summary_taxes.append(existing_summary.account_tax)
                    else:
                        # Create
                        summary_parameters = {
                            'account_move_line': account_move_line,
                            'invoice': self,
                            'non_zero_rate': True,
                        }
                        summary_class = self.env['l10n.hu.invoice.summary']
                        summary_result = summary_class.get_values_from_account_move_line(summary_parameters)
                        if len(summary_result['error_list']) == 0:
                            new_summary = summary_class.create(summary_result['crud_values'])

                            # Append to list
                            created_summaries.append(new_summary)
                            if new_summary.account_tax not in summary_taxes:
                                summary_taxes.append(new_summary.account_tax)

        # Now lets clean up
        used_taxes = set()
        for invoice_line in account_move.invoice_line_ids:
            for tax in invoice_line.tax_ids:
                used_taxes.add(tax)

        # Get summaries by create_date desc
        summaries = self.env['l10n.hu.invoice.summary'].search([
            ('invoice', '=', self.id)
        ], order='create_date desc')

        clean_taxes = set()
        for summary in summaries:
            # Delete not used taxes
            if summary.account_tax not in used_taxes:
                deleted_summaries.append(summary)
                summary.sudo().unlink()
            # Delete duplicate taxes
            elif summary.account_tax in clean_taxes:
                deleted_summaries.append(summary)
                summary.sudo().unlink()
            else:
                clean_taxes.add(summary.account_tax)

        # Finalize result
        result = {
            'account_move_taxes': account_move_taxes,
            'created_summaries': created_summaries,
            'deleted_summaries': deleted_summaries,
            'invoice_taxes': invoice_taxes,
            'invoice_taxes_0_percent': invoice_taxes_0_percent,
            'not_yet_managed_taxes': not_yet_managed_taxes,
            'summary_taxes': summary_taxes,
            'updated_summaries': updated_summaries,
        }

        # Return result
        # raise exceptions.UserError("get_account_move_pull_values_invoice_summary END" + str(result))
        return result

    @api.model
    def get_account_move_pull_values_supplier(self, account_move=None):
        """ Get supplier values

        :return: dictionary
        """
        # Initialize variables
        supplier_address_building = ""
        supplier_address_country_code = ""
        supplier_address_country_id = False
        supplier_address_country_name = ""
        supplier_address_country_state_name = ""
        supplier_address_country_state_code = ""
        supplier_address_district = ""
        supplier_address_door = ""
        supplier_address_floor = ""
        supplier_address_house_number = ""
        supplier_address_lot_number = ""
        supplier_address_public_place_name = ""
        supplier_address_public_place_type = ""
        supplier_address_postal_code = ""
        supplier_address_settlement = ""
        supplier_address_staircase = ""
        supplier_address_street = ""
        supplier_address_street2 = ""
        supplier_address_type = ""
        error_text = ""

        # Set invoice_direction
        if account_move.move_type in ['in_invoice', 'in_refund']:
            invoice_direction = 'inbound'
        elif account_move.move_type in ['out_invoice', 'out_refund']:
            invoice_direction = 'outbound'
        else:
            invoice_direction = False

        # Supplier
        if invoice_direction == 'inbound':
            supplier = account_move.partner_id
            supplier_name = supplier.display_name
        elif invoice_direction == 'outbound':
            supplier = account_move.company_id.partner_id
            supplier_name = supplier.display_name
        else:
            return {}

        # Supplier vat group
        """
        if supplier.l10n_hu_l10n_hu_vat_group:
            supplier_vat_group_id = supplier.l10n_hu_l10n_hu_vat_group.id
            supplier_vat_group_number = supplier.l10n_hu_l10n_hu_vat_group.name
            supplier_vat_group_member_number = supplier.l10n_hu_l10n_hu_vat
        else:
            supplier_vat_group_id = False
            supplier_vat_group_number = ""
            supplier_vat_group_member_number = ""
        """

        # Supplier address
        if supplier.country_id and supplier.street:
            supplier_address_type = 'simple'
            supplier_address_country_id = supplier.country_id.id
            supplier_address_country_code = supplier.country_id.code
            supplier_address_country_name = supplier.country_id.name
            supplier_address_postal_code = supplier.zip
            supplier_address_settlement = supplier.city
            supplier_address_street = supplier.street
            supplier_address_street2 = supplier.street2
        else:
            error_text += "\n" + _("Supplier address has no country!")

        # Supplier bank account
        if invoice_direction == 'inbound':
            supplier_bank_account = account_move.partner_bank_id
            supplier_bank_account_number = supplier_bank_account.acc_number
        elif invoice_direction == 'outbound':
            supplier_bank_account = account_move.l10n_hu_company_bank_account
            supplier_bank_account_number = supplier_bank_account.acc_number
        else:
            supplier_bank_account = False
            supplier_bank_account_number = False

        # Assemble result
        result = {
            'supplier': supplier.id,
            'supplier_address_building': supplier_address_building,
            'supplier_address_country': supplier_address_country_id,
            'supplier_address_country_state_name': supplier_address_country_state_name,
            'supplier_address_country_state_code': supplier_address_country_state_code,
            'supplier_address_country_name': supplier_address_country_name,
            'supplier_address_country_code': supplier_address_country_code,
            'supplier_address_district': supplier_address_district,
            'supplier_address_door': supplier_address_door,
            'supplier_address_floor': supplier_address_floor,
            'supplier_address_house_number': supplier_address_house_number,
            'supplier_address_lot_number': supplier_address_lot_number,
            'supplier_address_postal_code': supplier_address_postal_code,
            'supplier_address_public_place_name': supplier_address_public_place_name,
            'supplier_address_public_place_type': supplier_address_public_place_type,
            'supplier_address_settlement': supplier_address_settlement,
            'supplier_address_staircase': supplier_address_staircase,
            'supplier_address_street': supplier_address_street,
            'supplier_address_street2': supplier_address_street2,
            'supplier_address_type': supplier_address_type,
            'supplier_bank_account': supplier_bank_account,
            'supplier_bank_account_number': supplier_bank_account_number,
            'supplier_incorporation': supplier.l10n_hu_incorporation,
            'supplier_community_vat_number': supplier.vat,
            'supplier_name': supplier_name,
            'supplier_vat_status': supplier.l10n_hu_vat_status,
            'supplier_tax_number': supplier.l10n_hu_vat,
            # 'supplier_vat_group': supplier_vat_group_id,
            # 'supplier_vat_group_number': supplier_vat_group_number,
            # 'supplier_vat_group_member_number': supplier_vat_group_member_number,
        }

        # Return result
        return result

    @api.model
    def get_account_move_push_allowed(self):
        """ Determine if push to account move is allowed or not

        Meant to be overridden by super

        :return: True or False
        """
        # Initialize variables
        points = 0
        result = False

        # Some safeguard checks
        if not self.account_move:
            return result

        # Check state
        if self.account_move.state == 'draft':
            points += 1

        # Check journal type
        if self.account_journal and self.account_journal.type in ['purchase', 'sale']:
            points += 1

        # Check journal invoice setting
        if self. account_journal and self.account_journal.l10n_hu_invoice_enabled:
            points += 1

        # Evaluate points
        if points == 3:
            result = True

        # Return result
        return result

    @api.model
    def get_account_move_push_values(self):
        """ Get data from invoice and push them to account move

        :return: dictionary
        """
        # Initialize variables
        account_move_values = {}
        result = {}

        # Some safeguard checks
        if not self.account_move:
            return result

        # Set account_move
        account_move = self.account_move

        # Collect account move lines
        account_move_line_values_list = []
        for invoice_line in self.invoice_line:
            move_line_parameters = {
                'invoice_line': invoice_line
            }
            move_line_result = self.get_account_move_line_push_values(move_line_parameters)
            account_move_line_values_list.append(move_line_result['account_move_line_values'])

        # Update account_move_values
        account_move_values.update({
            'date': self.invoice_delivery_date,
            'invoice_date': self.invoice_issue_date,
            'invoice_date_due': self.payment_date,
            'invoice_delivery_date': self.invoice_delivery_date,
            'invoice_line_ids': [(0, 0, values) for values in account_move_line_values_list],
            'narration': self.comment,
        })

        # Update result
        result.update({
            'account_move': account_move,
            'account_move_values': account_move_values
        })

        # Return result
        return result

    @api.model
    def get_account_move_line_push_values(self, values):
        """ Get data from invoice line to push them account move line

        :param values: dictionary

        :return: dictionary
        """
        # Initialize variables
        account_move_line_values = {}
        result = {}

        # Some safeguard checks
        if values.get('invoice_line'):
            invoice_line = values['invoice_line']
        else:
            invoice_line = False

        # name
        name = invoice_line.line_description

        # quantity
        quantity = invoice_line.quantity

        # price_unit
        price_unit = invoice_line.unit_price

        # tax
        if invoice_line.account_tax:
            account_tax_id = invoice_line.account_tax.id
        else:
            account_tax_id = False

        # Update account_move_line_values
        account_move_line_values.update({
            'name': name,
            'quantity': quantity,
            'price_unit': price_unit,
        })
        if account_tax_id:
            account_move_line_values.update({
                'tax_ids': [(4, account_tax_id, False)],
            })

        # Update result
        result.update({
            'account_move_line_values': account_move_line_values
        })

        # Return result
        return result

    @api.model
    def get_existing_invoice(self, values):
        """ Get existing invoice

        We need an invoice number and a supplier taxpayer id to make the search
        We search in account moves
        We search differently for inbound and outbound invoices
        We also check and fix the invoice record linked to the account move

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("get_existing_invoice BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        result = {}
        taxpayer_id_pattern = re.compile("[0-9]")

        # Company
        if values.get('company'):
            company = values['company']
            company_id = company.id
            company_partner = company.partner_id
            company_taxpayer_id = False
            try:
                company_taxpayer_id = company_partner.l10n_hu_vat[:8]
            except:
                error_list.append("could not set company_taxpayer_id")
            if company_taxpayer_id and len(company_taxpayer_id) != 8:
                error_list.append("company_taxpayer_id must be 8 characters!")
            company_taxpayer_id_match = taxpayer_id_pattern.match(company_taxpayer_id)
            if not company_taxpayer_id_match:
                error_list.append("First 8 characters of company_taxpayer_id must be a number (0-9)!")
        else:
            company = False
            company_id = False
            company_partner = False
            company_taxpayer_id = False
            error_list.append("company not found in values")

        # Invoice direction
        if values.get('invoice_direction', ""):
            invoice_direction = values['invoice_direction'].lower()
        else:
            invoice_direction = False
            error_list.append("invoice direction not provided!")

        # Invoice number
        if values.get('invoice_number'):
            invoice_number = values['invoice_number']
        else:
            invoice_number = False
            error_list.append("invoice_number not found in values!")

        # Customer taxpayer id
        if values.get('customer_tax_number'):
            customer_taxpayer_id = values['customer_tax_number'][:8]
            if len(customer_taxpayer_id) != 8:
                error_list.append("customer_taxpayer_id must be 8 characters!")
            customer_taxpayer_id_match = taxpayer_id_pattern.match(customer_taxpayer_id)
            if not customer_taxpayer_id_match:
                error_list.append("First 8 characters of customer_taxpayer_id must be a number (0-9)!")
        else:
            customer_taxpayer_id = False

        # Supplier taxpayer id
        if values.get('supplier_tax_number'):
            supplier_taxpayer_id = values['supplier_tax_number'][:8]
            if len(supplier_taxpayer_id) != 8:
                error_list.append("supplier_taxpayer_id must be 8 characters!")
            supplier_taxpayer_id_match = taxpayer_id_pattern.match(supplier_taxpayer_id)
            if not supplier_taxpayer_id_match:
                error_list.append("First 8 characters of supplier_taxpayer_id must be a number (0-9)!")
        else:
            supplier_taxpayer_id = False

        # Set customer
        if invoice_direction == 'inbound' and company_partner:
            customer = company_partner
            customer_id = company_partner.id
        elif invoice_direction == 'outbound' and customer_taxpayer_id:
            customer = self.env['res.partner'].sudo().search([
                ('is_company', '=', True),
                ('l10n_hu_l10n_hu_vat', 'like', customer_taxpayer_id)
            ], limit=1)
            if customer:
                customer_id = customer.id
            else:
                customer_id = False
        else:
            customer = False
            customer_id = False

        # Find supplier
        if invoice_direction == 'inbound' and supplier_taxpayer_id:
            supplier = self.env['res.partner'].sudo().search([
                ('is_company', '=', True),
                ('l10n_hu_l10n_hu_vat', 'like', supplier_taxpayer_id)
            ], limit=1)
            if supplier:
                supplier_id = supplier.id
            else:
                supplier_id = False
        elif invoice_direction == 'outbound' and company_partner:
            supplier = company_partner
            supplier_id = company_partner.id
        else:
            supplier = False
            supplier_id = False

        # Scenario 1: INBOUND invoice
        if invoice_direction == 'inbound' and invoice_number and supplier_id:
            account_move = self.env['account.move'].sudo().search([
                ('company_id', '=', company_id),
                ('journal_id.type', '=', 'purchase'),
                ('partner_id', '=', supplier_id),
                ('ref', '=', invoice_number),
            ], order='id asc')
            if len(account_move) == 1:
                pass
            elif len(account_move) > 1:
                account_move = account_move[0]
                error_text = "multiple inbound invoices found!"
                error_text += " - supplier_id:" + str(supplier_id)
                error_text += " - supplier_taxpayer_id:" + str(supplier_taxpayer_id)
                error_text += " - invoice_number:" + str(invoice_number)
                error_list.append(error_text)
            else:
                pass
        # Scenario 2: OUTBOUND invoice
        elif invoice_direction == 'outbound' and invoice_number:
            # Search first for name (this is for outgoing invoices created locally)
            account_move = self.env['account.move'].sudo().search([
                ('journal_id.type', '=', 'sale'),
                ('company_id', '=', company_id),
                ('name', '=', invoice_number),
            ], order='id asc')
            # THEN search for ref (this is for outgoing invoice created in other systems)
            if not account_move:
                account_move = self.env['account.move'].sudo().search([
                    ('journal_id.type', '=', 'sale'),
                    ('company_id', '=', company_id),
                    ('ref', '=', invoice_number),
                ], order='id asc')

            # Check result
            if len(account_move) == 1:
                pass
            elif len(account_move) > 1:
                account_move = account_move[0]
                error_text = "multiple outbound invoices found!"
                error_text += " - supplier_id:" + str(supplier_id)
                error_text += " - supplier_taxpayer_id:" + str(supplier_taxpayer_id)
                error_text += " - invoice_number:" + str(invoice_number)
                error_list.append(error_text)
            else:
                pass
        else:
            account_move = False

        # Make sure we have an invoice
        if account_move and account_move.l10n_hu_invoice:
            invoice = account_move.l10n_hu_invoice
        elif account_move:
            account_move.sudo().write()
            invoice = account_move.l10n_hu_invoice
        else:
            invoice = False
            debug_list.append("invoice not found")

        # Make sure invoice number if filled out on the invoice, and it is the same
        if invoice_direction == 'inbound' \
                and account_move \
                and account_move.journal_id \
                and account_move.journal_id.type == 'purchase' \
                and account_move.ref == invoice_number \
                and invoice \
                and (not invoice.invoice_number or account_move.ref != invoice.invoice_number):
            invoice.sudo().write({
                'invoice_number': invoice_number
            })
            debug_list.append("updated invoice_number field on invoice record")

        # account_journal
        if account_move:
            account_journal = account_move.journal_id
        else:
            account_journal = False

        # Update result
        result.update({
            'account_journal': account_journal,
            'account_move': account_move,
            'company': company,
            'company_id': company_id,
            'company_partner': company_partner,
            'company_taxpayer_id': company_taxpayer_id,
            'customer': customer,
            'customer_id': customer_id,
            'customer_taxpayer_id': customer_taxpayer_id,
            'debug_list': debug_list,
            'error_list': error_list,
            'invoice': invoice,
            'invoice_direction': invoice_direction,
            'invoice_number': invoice_number,
            'supplier': supplier,
            'supplier_id': supplier_id,
            'supplier_taxpayer_id': supplier_taxpayer_id,
        })

        # Return result
        # raise exceptions.UserError("get_existing_invoice END" + str(result))
        return result

    @api.model
    def get_required_fields(self):
        """ Get required minimum fields

        :return list of field names
        """
        # result
        result = [
            'currency_code',
            'exchange_rate',
            'invoice_appearance',
            'invoice_category',
            'invoice_delivery_date',
            'supplier_tax_number',
        ]

        # Return result
        return result

    @api.model
    def get_write_protected_fields(self):
        """ Get fields that are protected by write

        If the account move has been posted we should not modify some fields

        There can be exceptions, eg: code errors, manual exceptions, etc

        Can be overridden by super calls

        :return: list of field names
        """
        # Assemble result
        result = [
            'currency_code',
            'customer_community_vat_number',
            'customer_tax_number',
            'customer_third_state_tax_id',
            'exchange_rate',
            'invoice_appearance',
            'invoice_category',
            'invoice_delivery_date',
            'invoice_number',
            'invoice_issue_date',
            'payment_date',
            'supplier_community_vat_number',
            'supplier_tax_number',
        ]

        # Return result
        return result

    @api.model
    def manage_write_values(self, values):
        """ This method gets all values from write method and adds/removes values when necessary

        Main purpose is to manage (remove from values) write protected fields

        Can be overridden by super calls

        :param values: dictionary

        :return: dictionary
        """
        # Initialize variables
        result = values or {}

        # Get write protected fields
        write_protected_fields = self.get_write_protected_fields()

        # Check account_move
        if self.account_move \
                and self.account_move.state != 'draft' \
                and self.account_move.move_type in ['out_invoice', 'out_refund'] \
                and self.locked:
            is_write_protected = True
        elif self.account_move \
                and self.account_move.move_type in ['in_invoice', 'in_refund'] \
                and self.locked:
            is_write_protected = True
        else:
            is_write_protected = False

        # Iterate on dictionary values
        for key in list(result):
            # Remove write protected fields if account move is posted
            if is_write_protected and key in write_protected_fields:
                result.pop(key)

        # Return result
        return result

    @api.model
    def pull_from_account_move(self):
        """ Pull data from account move """
        # Get values
        values = self.get_account_move_pull_values()
        # raise exceptions.UserError(str(values))

        # Write
        self.write(values)

        # Return result
        return

    @api.model
    def push_to_account_move(self):
        """ Push data to account move """
        # Determine if push is allowed
        push_allowed = self.get_account_move_push_allowed()

        # Write
        if push_allowed:
            # Get values
            values_result = self.get_account_move_push_values()

            # Remove all lines
            try:
                account_move_lines = self.env['account.move.line'].sudo().search([
                    ('move_id', '=', self.account_move.id)
                ])
                for account_move_line in account_move_lines:
                    account_move_line.sudo().unlink()
            except:
                pass

            # Do write
            self.account_move.sudo().write(values_result.get('account_move_values'))

        # Return result
        return

    @api.model
    def run_healthcheck(self, values=None):
        """ Run healthcheck on an invoice

        STEP 1: check system
        STEP 2: check invoice header
        STEP 3: check invoice lines
        STEP 4: check invoice summary

        :return: dictionary
        """
        # Initialize variables
        debug_list = []
        error_list = []
        healthcheck_scope = {}
        info_list = []
        result = {}
        success_list = []
        warning_list = []

        # account_move
        if values.get('account_move'):
            account_move = values['account_move']
            healthcheck_scope.update({
                'account_move': account_move
            })
        else:
            account_move = False

        # invoice
        if values.get('invoice'):
            invoice = values['invoice']
            healthcheck_scope.update({
                'invoice': invoice
            })
        elif len(self) == 1:
            invoice = self
            healthcheck_scope.update({
                'invoice': invoice
            })
        else:
            invoice = False

        # invoice_values
        if values.get('invoice_values'):
            healthcheck_scope.update({
                'invoice_values': values['invoice_values']
            })
        else:
            pass

        # invoice_header_result
        invoice_header_result = self.run_healthcheck_invoice_header(healthcheck_scope)
        debug_list += invoice_header_result['debug_list']
        error_list += invoice_header_result['error_list']
        info_list += invoice_header_result['info_list']
        success_list += invoice_header_result['success_list']
        warning_list += invoice_header_result['warning_list']

        # Prepare list
        # TODO: invoice_line_values (list of dictionaries describing an invoice line) are not yet handled!
        healthcheck_line_scopes = []
        if account_move and not invoice:
            for account_move_line in account_move.invoice_line_ids:
                healthcheck_line_scopes.append({
                    'account_move_line': account_move_line,
                    'invoice_line': False,
                })
        elif invoice:
            for invoice_line in invoice.invoice_line:
                healthcheck_line_scopes.append({
                    'account_move_line': invoice_line.account_move_line,
                    'invoice_line': invoice_line,
                })
        else:
            pass

        # invoice_line_result
        for healthcheck_line_scope in healthcheck_line_scopes:
            healthcheck_line_scope.update(healthcheck_scope)
            invoice_line_result = self.run_healthcheck_invoice_line(healthcheck_line_scope)
            debug_list += invoice_line_result['debug_list']
            error_list += invoice_line_result['error_list']
            info_list += invoice_line_result['info_list']
            success_list += invoice_line_result['success_list']
            warning_list += invoice_line_result['warning_list']

        # result
        result.update({
            'debug_count': len(debug_list),
            'debug_list': debug_list,
            'error_count': len(error_list),
            'error_list': error_list,
            'healthcheck_scope': healthcheck_scope,
            'info_count': len(info_list),
            'info_list': info_list,
            'invoice_header_result': invoice_header_result,
            'type': 'success',
            'success_count': len(success_list),
            'success_list': success_list,
            'warning_count': len(warning_list),
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result

    @api.model
    def run_healthcheck_invoice_header(self, values):
        """ Run healthcheck on the header of an invoice

        Checklist:
            01) l10n_hu_invoice_journal: checks if the selected journal is enabled for hungarian invoicing
            02) foreign_currency: checks if foreign currency is used
            03) customer_l10n_hu_vat: checks if the customer's VAT format is valid
            04) customer_address: checks the customer's address
            05) customer_geolocation: checks the customer's geolocation address
            06) supplier_bank_account: checks the bank of the supplier
            07) invoice_due_date: checks the due date
            08) invoice_document_type: checks the document type
            09) invoice_delivery_date: checks the delivery date
            10) currency_rate: checks the currency rate
            11) invoice_line_set: checks there is at least one invoice line
            12) eu_oss_eligible: EU OSS eligible warning
            13) eu_oss_app_status: checks if app is needed and installed
            14) eu_oss_commercial_partner: checks if commercial partner is EU OSS eligible and has fiscal position
            15) eu_oss_taxes: checks if invoice EU OSS eligibility and taxes
            16) customer_tax_number: checks scenarios for customer tax number

        TODO: expand checklist

        :param: values dictionary

        :return: dictionary
        """
        # raise exceptions.UserError(str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        healthcheck_results = []
        result = {}
        success_list = []
        warning_list = []

        # account_move
        account_move = values.get('account_move')

        # invoice_values
        invoice_values = values.get('invoice_values')

        # invoice
        invoice = values.get('invoice')

        # customer
        if account_move:
            customer = account_move.partner_id
        elif invoice:
            customer = invoice.customer
        else:
            customer = False

        # 01) l10n_hu_invoice_journal
        l10n_hu_invoice_journal = {
            'category': 'invoice_header',
            'description': _("Hungarian invoicing is enabled on the journal"),
            'name': _("HU Invoice Journal"),
            'technical_name': 'l10n_hu_invoice_journal',
        }

        if account_move \
                and account_move.journal_id.l10n_hu_invoice_enabled \
                and account_move.journal_id.l10n_hu_technical_type == 'invoice':
            l10n_hu_invoice_journal.update({
                'account_move_result': True
            })
            info_list.append(_("Hungarian invoicing is enabled on the journal."))
            warning_list.append(_("The invoice will not be editable after confirming."))
        elif account_move \
                and account_move.journal_id.l10n_hu_technical_type != 'invoice':
            l10n_hu_invoice_journal.update({
                'account_move_result': False
            })
        else:
            pass

        if invoice_values:
            l10n_hu_invoice_journal.update({
                'invoice_values_result': True
            })
        else:
            pass

        if invoice and invoice.account_journal.l10n_hu_technical_type == 'invoice':
            l10n_hu_invoice_journal.update({
                'invoice_result': True
            })
        elif invoice and invoice.account_journal.l10n_hu_technical_type != 'invoice':
            l10n_hu_invoice_journal.update({
                'invoice_result': False
            })
        else:
            pass

        if account_move and invoice:
            if l10n_hu_invoice_journal['account_move_result'] == l10n_hu_invoice_journal['invoice_result']:
                success_list.append(_("Journal hungarian invoicing enabled ok"))

        # Append to healthcheck_results
        healthcheck_results.append(l10n_hu_invoice_journal)

        # 02) foreign_currency
        foreign_currency = {
            'category': 'invoice_header',
            'description': _("The invoice is in foreign currency"),
            'name': _("Foreign currency"),
            'technical_name': 'foreign_currency',
        }

        if account_move \
                and account_move.currency_id != account_move.company_id.currency_id:
            foreign_currency.update({
                'account_move_result': True
            })
        else:
            foreign_currency.update({
                'account_move_result': False
            })

        if invoice_values:
            pass

        if invoice \
                and invoice.currency_code != invoice.company_currency_name:
            foreign_currency.update({
                'invoice_result': True
            })
        elif invoice \
                and invoice.currency_code == invoice.company_currency_name:
            foreign_currency.update({
                'invoice_result': False
            })
        else:
            pass

        # Append to healthcheck_results
        healthcheck_results.append(foreign_currency)

        # 03) customer_l10n_hu_vat
        customer_l10n_hu_vat = {
            'category': 'invoice_header',
            'description': _("Hungarian VAT format is ok"),
            'name': _("Customer HU VAT"),
            'technical_name': 'customer_l10n_hu_vat',
        }

        if customer and customer.country_id.code == 'HU' \
                and customer.l10n_hu_vat \
                and customer.l10n_hu_vat_status == 'domestic':
            check_l10n_hu_vat = True
        else:
            check_l10n_hu_vat = False

        if check_l10n_hu_vat:
            l10n_hu_vat_ok = customer.l10n_hu_get_is_valid_l10n_hu_vat()

            if account_move and l10n_hu_vat_ok:
                customer_l10n_hu_vat.update({
                    'account_move_result': True
                })
            else:
                customer_l10n_hu_vat.update({
                    'account_move_result': False
                })

            if invoice and l10n_hu_vat_ok:
                customer_l10n_hu_vat.update({
                    'invoice_result': True
                })
            else:
                customer_l10n_hu_vat.update({
                    'invoice_result': False
                })
        else:
            l10n_hu_vat_ok = True
            customer_l10n_hu_vat.update({
                'account_move_result': True,
                'invoice_result': True
            })

        if account_move and invoice:
            if l10n_hu_vat_ok \
                    and customer_l10n_hu_vat['account_move_result'] == customer_l10n_hu_vat['invoice_result']:
                success_list.append(_("Hungarian VAT format ok"))
            else:
                error_list.append(_("Invalid hungarian VAT number format! Sample: 12345678-9-10"))
        else:
            info_list.append(_("Hungarian VAT format validation skipped"))

        # Append to healthcheck_results
        healthcheck_results.append(customer_l10n_hu_vat)

        # 04) customer_address
        customer_address = {
            'category': 'invoice_header',
            'description': _("Customer address details"),
            'name': _("Customer Address"),
            'technical_name': 'customer_address',
        }

        # Initialize variables
        am_address_details = ""
        ni_address_details = ""

        if account_move and account_move.partner_id:
            am_address_details = _("Country") + ": " + str(account_move.partner_id.country_id.code) + "\n"
            am_address_details += _("City") + ": " + str(account_move.partner_id.city) + "\n"
            am_address_details += _("Street") + ": " + str(account_move.partner_id.street)
            if not account_move.partner_id.country_id \
                    or not account_move.partner_id.city \
                    or not account_move.partner_id.street:
                # error_text
                error_text = _("The customer must have at least country, city and street information!")
                am_address_details = error_text + "\n" + am_address_details
                error_list.append(am_address_details)
                customer_address.update({
                    'account_move_result': 'error'
                })
            else:
                debug_list.append(am_address_details)
                customer_address.update({
                    'account_move_result': 'ok'
                })
        else:
            customer_address.update({
                'account_move_result': 'ok'
            })

        if invoice and invoice.customer:
            if invoice.customer_address_type == 'simple' \
                    and (not invoice.customer_address_country_code
                         or not invoice.customer_address_settlement
                         or not invoice.customer_address_street):
                # details
                ni_address_details = _("Country") + ": " + str(invoice.customer_address_country_code) + "\n"
                ni_address_details += _("City") + ": " + str(invoice.customer_address_settlement) + "\n"
                ni_address_details += _("Street") + ": " + str(invoice.customer_address_street)

                # error_text
                error_text = _("The customer must have at least country, city and street information!")
                ni_error_details = error_text + "\n" + ni_address_details
                error_list.append(ni_error_details)
                customer_address.update({
                    'invoice_result': 'error'
                })
            else:
                customer_address.update({
                    'invoice_result': 'ok'
                })

            if invoice.customer_address_type == 'detailed' \
                    and (not invoice.customer_address_country_code
                         or not invoice.customer_address_settlement
                         or not invoice.customer_address_public_place_name
                         or not invoice.customer_address_public_place_type
                         or not invoice.customer_address_house_number):
                # details
                ni_address_details = _("Country") + ": " + str(invoice.customer_address_country_code) + "\n"
                ni_address_details += _("City") + ": " + str(invoice.customer_address_settlement) + "\n"
                ni_address_details += _("Public Place") + ": " + str(invoice.customer_address_public_place_name)
                ni_address_details += _("Place Type") + ": " + str(invoice.customer_address_public_place_type)
                ni_address_details += _("House Number") + ": " + str(invoice.customer_address_house_number)

                # error_text
                error_text = _("The customer must have at least country, city and street information!")
                ni_error_details = error_text + "\n" + ni_address_details
                error_list.append(ni_error_details)
                customer_address.update({
                    'invoice_result': 'error'
                })
            else:
                customer_address.update({
                    'invoice_result': 'ok'
                })

            # customer_address_type is empty
            if not invoice.customer_address_type or len(invoice.customer_address_type) == 0:
                # details
                ni_address_details = _("Country") + ": " + str(invoice.customer_address_country_code) + "\n"
                ni_address_details += _("City") + ": " + str(invoice.customer_address_settlement) + "\n"
                ni_address_details += _("Street") + ": " + str(invoice.customer_address_street)

                # error_text
                error_text = _("The customer must have at least country, city and street information!")
                ni_error_details = error_text + "\n" + ni_address_details
                error_list.append(ni_error_details)
                customer_address.update({
                    'invoice_result': 'error'
                })
        else:
            customer_address.update({
                'invoice_result': 'ok'
            })

        if am_address_details == ni_address_details:
            customer_address.update({
                'consistency_result': True
            })
        else:
            customer_address.update({
                'consistency_result': False
            })

        # Append to healthcheck_results
        healthcheck_results.append(customer_address)

        # 05) customer_geolocation
        customer_geolocation = {
            'category': 'invoice_header',
            'description': _("Customer geolocation address status"),
            'name': _("Customer Geolocation"),
            'technical_name': 'customer_geolocation_address',
        }

        # Set has_geolocation_address
        geolocation_installed = self.l10n_hu_geolocation_installed()

        if account_move and account_move.partner_id:
            if geolocation_installed and account_move.partner_id \
                    and account_move.partner_id.commercial_partner_id.country_id \
                    and account_move.partner_id.l10n_hu_address:
                account_move_has_geolocation_address = True
                customer_address.update({
                    'account_move_result': 'ok'
                })
            elif geolocation_installed and account_move.partner_id \
                    and not account_move.partner_id.commercial_partner_id.country_id:
                account_move_has_geolocation_address = True
                customer_address.update({
                    'account_move_result': 'ok'
                })
            else:
                account_move_has_geolocation_address = False
                customer_address.update({
                    'account_move_result': 'error'
                })

        # Append to healthcheck_results
        healthcheck_results.append(customer_geolocation)

        # 06) supplier_bank_account
        supplier_bank_account = {
            'category': 'invoice_header',
            'description': _("Supplier bank account should be set"),
            'name': _("Supplier Bank Account"),
            'technical_name': 'supplier_bank_account',
        }

        # account_move
        if account_move and account_move.l10n_hu_company_bank_account:
            supplier_bank_account.update({
                'account_move_result': 'ok',
                'account_move_record': account_move.l10n_hu_company_bank_account,
                'account_move_value': account_move.l10n_hu_company_bank_account.acc_number,
            })
        else:
            supplier_bank_account.update({
                'account_move_result': 'error',
                'account_move_record': False,
                'account_move_value': False,
            })

        # invoice
        if invoice and invoice.supplier_bank_account_number:
            supplier_bank_account.update({
                'invoice_result': 'ok',
                'invoice_record': invoice.supplier_bank_account,
                'invoice_value': invoice.supplier_bank_account_number,
            })
        else:
            supplier_bank_account.update({
                'invoice_result': 'error',
                'invoice_record': False,
                'invoice_value': False,
            })

        # TODO check data consistency

        # Append to healthcheck_results
        healthcheck_results.append(supplier_bank_account)

        # 07) invoice_due_date
        invoice_due_date = {
            'category': 'invoice_header',
            'description': _("Invoice due validation"),
            'name': _("Invoice Due Date"),
            'technical_name': 'invoice_due_date',
        }

        # account_move TODO we only check if it is filled out for now, later check value
        if account_move:
            # Set has_date_due
            if account_move.invoice_payment_term_id or account_move.invoice_date_due:
                has_date_due = True
            else:
                has_date_due = False

            if has_date_due:
                invoice_due_date.update({
                    'account_move_result': 'ok',
                    'account_move_value': has_date_due,
                })
            else:
                invoice_due_date.update({
                    'account_move_result': 'error',
                    'account_move_value': has_date_due,
                })
                error_list.append(_("Payment term or due date must be set!"))
        else:
            invoice_due_date.update({
                'account_move_result': 'error',
            })

        # invoice
        if invoice:
            if invoice.invoice_status == 'draft':
                invoice_due_date.update({
                    'invoice_result': 'ok',
                    'invoice_value': invoice.payment_date,
                })
            elif invoice.invoice_status != 'draft' and invoice.payment_date:
                invoice_due_date.update({
                    'invoice_result': 'ok',
                    'invoice_value': invoice.payment_date,
                })
            else:
                invoice_due_date.update({
                    'invoice_result': 'error',
                    'invoice_value': invoice.payment_date,
                })
                error_list.append(_("Invoice payment date must be set!"))
        else:
            invoice_due_date.update({
                'invoice_result': 'error',
            })

        # TODO check data consistency

        # Append to healthcheck_results
        healthcheck_results.append(invoice_due_date)

        # 08) invoice_document_type
        invoice_document_type = {
            'category': 'invoice_header',
            'description': _("Invoice document type validation"),
            'name': _("Invoice Document Type"),
            'technical_name': 'invoice_document_type',
        }

        # account_move TODO we only check if it is filled out for now, later check value
        if account_move:
            if account_move.l10n_hu_document_type:
                invoice_document_type.update({
                    'account_move_result': 'ok',
                    'account_move_record': account_move.l10n_hu_document_type,
                    'account_move_value': account_move.l10n_hu_document_type,
                })

            else:
                invoice_document_type.update({
                    'account_move_result': 'error',
                    'account_move_value': False,
                })
                error_list.append(_("Document type can not be empty!"))
        else:
            invoice_document_type.update({
                'account_move_result': 'error',
            })

        # invoice
        if invoice:
            if invoice.document_type:
                invoice_document_type.update({
                    'invoice_result': 'ok',
                    'invoice_value': invoice.document_type,
                })
            else:
                invoice_document_type.update({
                    'invoice_result': 'error',
                    'invoice_value': invoice.document_type,
                })

        # TODO check data consistency

        # Append to healthcheck_results
        healthcheck_results.append(invoice_document_type)

        # 09) invoice_delivery_date
        invoice_delivery_date = {
            'category': 'invoice_header',
            'description': _("Invoice delivery date validation"),
            'name': _("Invoice Delivery Date"),
            'technical_name': 'invoice_delivery_date',
        }

        # account_move TODO we only check if it is filled out for now, later check value
        if account_move:
            # Set has_delivery_date_limit_breach
            if account_move.journal_id.l10n_hu_invoice_delivery_date_limit:
                has_breach = account_move.l10n_hu_get_invoice_delivery_date_limit_breach()
                if has_breach and account_move.journal_id.l10n_hu_technical_type == 'invoice':
                    has_delivery_date_limit_breach = True
                    error_list.append(_("Delivery date limit is breached!"))
                else:
                    has_delivery_date_limit_breach = False
            else:
                has_delivery_date_limit_breach = False

            if account_move.l10n_hu_invoice_delivery_date:
                invoice_delivery_date.update({
                    'account_move_has_delivery_date_limit_breach': has_delivery_date_limit_breach,
                    'account_move_result': 'ok',
                    'account_move_value': account_move.l10n_hu_invoice_delivery_date,
                })
            else:
                invoice_delivery_date.update({
                    'account_move_result': 'error',
                    'account_move_value': False,
                })
        else:
            invoice_delivery_date.update({
                'account_move_result': 'error',
            })

        # invoice
        if invoice:
            if invoice.invoice_delivery_date:
                invoice_delivery_date.update({
                    'invoice_result': 'ok',
                    'invoice_value': invoice.invoice_delivery_date,
                })
            else:
                invoice_delivery_date.update({
                    'invoice_result': 'error',
                    'invoice_value': invoice.invoice_delivery_date,
                })
                error_list.append(_("Invoice delivery date must be set!"))

        # TODO check data consistency

        # Append to healthcheck_results
        healthcheck_results.append(invoice_delivery_date)

        # 10) currency_rate
        currency_rate = {
            'category': 'invoice_header',
            'description': _("Currency rate validation"),
            'name': _("Currency Rate"),
            'technical_name': 'currency_rate',
        }

        # account_move TODO we only check if it is filled out for now, later check value
        if account_move:
            if account_move.l10n_hu_currency_rate \
                    and account_move.l10n_hu_currency_rate.name != account_move.l10n_hu_invoice_delivery_date \
                    and account_move.move_type not in ['in_invoice', 'in_refund']:
                has_currency_rate_date_difference = True
                warning_list.append(_("Currency rate can not be found for delivery date!"))
            else:
                has_currency_rate_date_difference = False

            if account_move.l10n_hu_currency_rate:
                currency_rate.update({
                    'account_move_has_currency_rate_date_difference': has_currency_rate_date_difference,
                    'account_move_result': 'ok',
                    'account_move_record': account_move.l10n_hu_currency_rate,
                    'account_move_value': account_move.l10n_hu_currency_rate.name,
                })
            else:
                currency_rate.update({
                    'account_move_result': 'error',
                    'account_move_value': False,
                })
        else:
            currency_rate.update({
                'account_move_result': 'error',
            })

        # invoice
        if invoice:
            if invoice.currency_rate:
                currency_rate.update({
                    'invoice_result': 'ok',
                    'invoice_value': invoice.currency_rate,
                })
            else:
                currency_rate.update({
                    'invoice_result': 'error',
                    'invoice_value': invoice.document_type,
                })

        # TODO check data consistency

        # Append to healthcheck_results
        healthcheck_results.append(currency_rate)

        # 11) invoice_line_set
        invoice_line_set = {
            'category': 'invoice_header',
            'description': _("Invoice must have at least one line"),
            'name': _("Invoice line set"),
            'technical_name': 'invoice_line_set',
        }

        # account_move
        if account_move:
            if len(account_move.invoice_line_ids) > 0:
                invoice_line_set.update({
                    'account_move_result': 'ok',
                    'account_move_value': len(account_move.invoice_line_ids),
                })
            else:
                invoice_line_set.update({
                    'account_move_result': 'error',
                    'account_move_value': 0,
                })
                error_list.append(_("Account move has no lines!"))

        # invoice
        if invoice:
            if len(invoice.invoice_line) > 0:
                invoice_line_set.update({
                    'invoice_result': 'ok',
                    'invoice_value': len(invoice.invoice_line),
                })
            else:
                invoice_line_set.update({
                    'invoice_result': 'error',
                    'invoice_value': 0,
                })
                error_list.append(_("Invoice no lines!"))

        # TODO check data consistency

        # Append to healthcheck_results
        healthcheck_results.append(invoice_line_set)

        # 12) eu_oss_eligible
        eu_oss_eligible = {
            'category': 'invoice_header',
            'description': _("EU OSS eligible warning"),
            'name': _("EU OSS eligible"),
            'technical_name': 'eu_oss_eligible',
        }

        # account_move
        if account_move:
            if account_move.l10n_hu_eu_oss_eligible:
                eu_oss_eligible.update({
                    'account_move_result': True,
                    'account_move_value': 'eligible',
                })
                warning_list.append(_("EU OSS eligible invoice"))
            else:
                eu_oss_eligible.update({
                    'account_move_result': True,
                    'account_move_value': 'not_eligible',
                })
                info_list.append(_("EU OSS not relevant"))

        # Append to healthcheck_results
        healthcheck_results.append(eu_oss_eligible)

        # 13) eu_oss_app_status
        eu_oss_app_status = {
            'category': 'invoice_header',
            'description': _("l10n_eu_oss app is needed and installed"),
            'name': _("EU OSS app status"),
            'technical_name': 'eu_oss_app_status',
        }

        # Check app
        l10n_eu_oss_module = self.env['ir.module.module'].sudo().search([
            ('name', '=', 'l10n_eu_oss'),
            ('state', '=', 'installed'),
        ])

        # account_move
        if account_move:
            if account_move.journal_id.l10n_hu_eu_oss_enabled \
                    and l10n_eu_oss_module:
                eu_oss_app_status.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'installed',
                })
                success_list.append(_("l10n_eu_oss app is required and installed"))
            elif not account_move.journal_id.l10n_hu_eu_oss_enabled:
                eu_oss_app_status.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'not_required',
                })
                success_list.append(_("l10n_eu_oss app is not required"))
            else:
                eu_oss_app_status.update({
                    'account_move_result': 'error',
                    'account_move_value': 'required_not_installed',
                })
                error_list.append(_("EU OSS: l10n_eu_oss app is required but not installed"))

        # Append to healthcheck_results
        healthcheck_results.append(eu_oss_app_status)

        # 14) eu_oss_commercial_partner
        eu_oss_commercial_partner = {
            'category': 'invoice_header',
            'description': _("Commercial partner is EU OSS eligible with proper fiscal position"),
            'name': _("EU OSS commercial partner"),
            'technical_name': 'eu_oss_commercial_partner',
        }

        # account_move
        if account_move:
            # commercial_partner
            try:
                commercial_partner = account_move.partner_id.commercial_partner_id
            except:
                commercial_partner = False

            # EU
            try:
                eu_country_group = self.env.ref('base.europe')
            except:
                eu_country_group = False

            if commercial_partner \
                    and commercial_partner.is_company:
                eu_oss_commercial_partner.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'company',
                })
                success_list.append(_("EU OSS: not relevant, commercial partner is a company"))
            elif commercial_partner \
                    and not commercial_partner.is_company \
                    and commercial_partner.country_id \
                    and commercial_partner.country_id == account_move.company_id.country_id:
                eu_oss_commercial_partner.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'not_company_same_country',
                })
                success_list.append(_("EU OSS not relevant, commercial partner and company country are the same"))
            elif commercial_partner \
                    and not commercial_partner.is_company \
                    and commercial_partner.country_id \
                    and commercial_partner.country_id not in eu_country_group.country_ids:
                eu_oss_commercial_partner.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'not_company_not_eu',
                })
                success_list.append(_("EU OSS not relevant, commercial partner is not from the EU"))
            elif commercial_partner \
                    and not commercial_partner.is_company \
                    and commercial_partner.country_id \
                    and eu_country_group \
                    and commercial_partner.country_id in eu_country_group.country_ids \
                    and account_move.journal_id \
                    and account_move.journal_id.l10n_hu_eu_oss_enabled \
                    and account_move.fiscal_position_id \
                    and account_move.fiscal_position_id.country_id == commercial_partner.country_id:
                eu_oss_commercial_partner.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'not_company_fiscal_position_ok',
                })
                success_list.append(_("EU OSS commercial partner fiscal position is ok"))
            elif account_move.journal_id \
                    and not account_move.journal_id.l10n_hu_eu_oss_enabled:
                eu_oss_commercial_partner.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'journal_eu_oss_disabled',
                })
                success_list.append(_("EU OSS disabled on the journal"))
            else:
                eu_oss_commercial_partner.update({
                    'account_move_result': 'error',
                    'account_move_value': 'eu_oss_error',
                })
                error_list.append(_("EU OSS inconsistent commercial partner and fiscal position country"))

        # Append to healthcheck_results
        healthcheck_results.append(eu_oss_commercial_partner)

        # 15) eu_oss_taxes
        eu_oss_taxes = {
            'category': 'invoice_header',
            'description': _("EU OSS taxes presence and consistency"),
            'name': _("EU OSS taxes"),
            'technical_name': 'eu_oss_taxes',
        }

        # account_move
        if account_move:
            try:
                customer_country = account_move.partner_id.commercial_partner_id.country_id
            except:
                customer_country = False

            # fiscal position taxes
            fiscal_position_taxes = []
            fiscal_position = account_move.fiscal_position_id
            if fiscal_position and fiscal_position.country_id:
                fiscal_position_country = fiscal_position.country_id
                for fiscal_position_tax in fiscal_position.tax_ids:
                    fiscal_position_taxes.append(fiscal_position_tax.tax_dest_id)
            else:
                fiscal_position_country = False

            # invoice taxes
            invoice_line_taxes = []
            invoice_line_tax_countries = []
            for invoice_line in account_move.invoice_line_ids:
                for invoice_line_tax in invoice_line.tax_ids:
                    if invoice_line_tax not in invoice_line_taxes:
                        invoice_line_taxes.append(invoice_line_tax)

                    try:
                        invoice_line_tax_country = invoice_line_tax.country_id
                    except:
                        invoice_line_tax_country = invoice_line_tax.company_id.partner_id.country_id

                    if invoice_line_tax_country not in invoice_line_tax_countries:
                        invoice_line_tax_countries.append(invoice_line_tax_country)

            # Tax consistency
            tax_error_count = 0
            for invoice_line_tax in invoice_line_taxes:
                if invoice_line_tax not in fiscal_position_taxes:
                    tax_error_count += 1

            if not account_move.l10n_hu_eu_oss_eligible:
                eu_oss_taxes.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'not_eligible',
                })
                success_list.append(_("EU OSS tax not eligible"))
            elif not account_move.fiscal_position_id:
                eu_oss_taxes.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'no_fiscal_position',
                })
                success_list.append(_("EU OSS tax no fiscal position"))
            elif fiscal_position_country \
                    and fiscal_position_country == customer_country \
                    and len(invoice_line_tax_countries) == 1 \
                    and invoice_line_tax_countries[0] == account_move.company_id.partner_id.country_id \
                    and tax_error_count == 0:
                eu_oss_taxes.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'single_country_matching_fiscal_position',
                })
                success_list.append(_("EU OSS taxes ok"))
            elif len(invoice_line_tax_countries) > 1:
                eu_oss_taxes.update({
                    'account_move_result': 'error',
                    'account_move_value': 'multiple_tax_country',
                })
                error_list.append(_("EU OSS taxes from multiple countries"))
            else:
                eu_oss_taxes.update({
                    'account_move_result': 'error',
                    'account_move_value': 'fiscal_position_tax_country_inconsistency',
                })
                warning_list.append(_("EU OSS inconsistent fiscal position and tax countries"))

        # TODO check data consistency

        # Append to healthcheck_results
        healthcheck_results.append(eu_oss_taxes)

        # 16) customer_tax_number
        customer_tax_number = {
            'name': _("Customer tax number"),
            'category': 'invoice_header',
            'description': _("Customer tax number setting"),
            'technical_name': 'customer_tax_number',
        }

        # account_move
        if account_move:
            try:
                customer = account_move.partner_id.commercial_partner_id
            except:
                customer = False

            try:
                customer_country = customer.country_id
            except:
                customer_country = False

            if customer and customer_country and customer_country.code == 'HU':
                is_hungarian = True
            else:
                is_hungarian = False

            # HU Domestic HU VAT set
            if is_hungarian \
                    and customer \
                    and customer.l10n_hu_vat_status == 'domestic' \
                    and customer.l10n_hu_vat:
                customer_tax_number.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'hungary_domestic_vat_set',
                })
                success_list.append(_("HU VAT ok"))
            # HU Domestic HU VAT empty
            elif is_hungarian \
                    and customer \
                    and customer.l10n_hu_vat_status == 'domestic' \
                    and customer.l10n_hu_vat in [False, '']:
                customer_tax_number.update({
                    'account_move_result': 'error',
                    'account_move_value': 'hungary_domestic_vat_empty',
                })
                error_list.append(_("HU VAT empty"))
            # Private person HU VAT empty
            elif customer \
                    and customer.l10n_hu_vat_status == 'private_person' \
                    and customer.l10n_hu_vat in [False, '']:
                customer_tax_number.update({
                    'account_move_result': 'ok',
                    'account_move_value': 'private_person_vat_empty',
                })
                success_list.append(_("HU VAT empty"))
            # Private person HU VAT set
            elif customer \
                    and customer.l10n_hu_vat_status == 'private_person' \
                    and customer.l10n_hu_vat not in [False, '']:
                customer_tax_number.update({
                    'account_move_result': 'warning',
                    'account_move_value': 'private_person_vat_set',
                })
                warning_list.append(_("Private person HU VAT is set"))
            # Other company VAT set
            elif customer \
                    and customer.l10n_hu_vat_status == 'other' \
                    and customer.is_company \
                    and customer.vat not in [False, '']:
                customer_tax_number.update({
                    'account_move_result': 'success',
                    'account_move_value': 'other_company_vat_set',
                })
                success_list.append(_("VAT is set"))
            # Other company VAT empty
            elif customer \
                    and customer.l10n_hu_vat_status == 'other' \
                    and customer.is_company \
                    and customer.vat in [False, '']:
                customer_tax_number.update({
                    'account_move_result': 'error',
                    'account_move_value': 'other_company_vat_empty',
                })
                error_list.append(_("VAT is empty"))
            # Other not company VAT set
            elif customer \
                    and customer.l10n_hu_vat_status == 'other' \
                    and not customer.is_company \
                    and customer.vat not in [False, '']:
                customer_tax_number.update({
                    'account_move_result': 'warning',
                    'account_move_value': 'other_not_company_vat_set',
                })
                success_list.append(_("VAT is empty"))
            # Other not company VAT empty
            elif customer \
                    and customer.l10n_hu_vat_status == 'other' \
                    and not customer.is_company \
                    and customer.vat in [False, '']:
                customer_tax_number.update({
                    'account_move_result': 'success',
                    'account_move_value': 'other_not_company_vat_empty',
                })
                success_list.append(_("VAT is empty"))
            # Other scenarios
            else:
                customer_tax_number.update({
                    'account_move_result': 'info',
                    'account_move_value': 'not_managed_scenario',
                })
                info_list.append(_("Not managed scenario"))

        # TODO check data consistency

        # Append to healthcheck_results
        healthcheck_results.append(customer_tax_number)

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'healthcheck_results': healthcheck_results,
            'info_list': info_list,
            'success_list': success_list,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result

    @api.model
    def run_healthcheck_invoice_line(self, values):
        """ Run healthcheck on a line of an invoice

        Checklist:
            01) line_tax_set: there should be exactly one tax on the line for HU taxes
            02) line_tax_l10n_hu: there should be exactly one l10n_hu compatible tax on the line for HU taxes

        TODO: expand checklist

        :return: dictionary
        """
        # raise exceptions.UserError(str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        healthcheck_results = []
        result = {}
        success_list = []
        warning_list = []

        # account_move
        account_move = values.get('account_move')

        # account_move_line
        account_move_line = values.get('account_move_line')

        # invoice_values
        invoice_values = values.get('invoice_values')

        # invoice_line_values
        invoice_line_values = values.get('invoice_line_values')

        # invoice
        invoice = values.get('invoice')

        # invoice_line
        invoice_line = values.get('invoice_line')

        # customer
        if account_move:
            customer = account_move.partner_id
        elif invoice:
            customer = invoice.customer
        else:
            customer = False

        # account_move_line_details
        if account_move_line:
            account_move_line_details = "[id:" + str(account_move_line.id) + "]"
            if account_move_line.product_id:
                account_move_line_details += " " + str(account_move_line.product_id.name)
            if account_move_line.quantity:
                account_move_line_details += " " + str(account_move_line.quantity)
            if account_move_line.product_uom_id:
                account_move_line_details += " " + str(account_move_line.product_uom_id.name)
        else:
            account_move_line_details = ""

        # invoice_line_details
        if invoice_line:
            invoice_line_details = "[id:" + str(invoice_line.id) + "]"
            if invoice_line.product:
                invoice_line_details += " " + str(invoice_line.product.name)
            if invoice_line.quantity:
                invoice_line_details += " " + str(invoice_line.quantity)
            if invoice_line.uom:
                invoice_line_details += " " + str(invoice_line.uom.name)
        else:
            invoice_line_details = ""

        # 01) line_tax_set
        line_tax_set = {
            'category': 'invoice_line',
            'description': _("There must be at least one tax set on the line"),
            'name': _("Invoice line tax"),
            'technical_name': 'line_tax_set',
        }

        # is_rounding_line
        is_rounding_line = account_move_line.l10n_hu_is_invoice_rounding_line()

        # Check account_move_line display_type
        if account_move_line and account_move_line.display_type not in ['line_note', 'line_section']:
            if is_rounding_line:
                line_tax_set.update({
                    'account_move_line_result': 'ok',
                    'account_move_line_value': False,
                })
                success_text = _("Rounding account move line, no tax necessary.")
                success_list.append(success_text)
            elif not account_move.l10n_hu_eu_oss_eligible \
                    and account_move_line.tax_ids \
                    and len(account_move_line.tax_ids) == 1:
                line_tax_set.update({
                    'account_move_line_result': 'ok',
                    'account_move_line_value': account_move_line.tax_ids[0],
                })
                success_text = _("There is one tax set on the account move line.")
                success_text += " " + str(account_move_line_details)
                success_list.append(success_text)
            elif not account_move.l10n_hu_eu_oss_eligible \
                    and account_move_line \
                    and account_move_line.tax_ids \
                    and len(account_move_line.tax_ids) > 1:
                line_tax_set.update({
                    'account_move_line_result': 'error',
                    'account_move_line_value': account_move_line.tax_ids,
                })
                error_text = _("More than one tax set on the account move line!")
                error_text += " " + str(account_move_line_details)
                error_list.append(error_text)
            elif not account_move_line.tax_ids:
                line_tax_set.update({
                    'account_move_line_result': 'error',
                    'account_move_line_value': 0,
                })
                error_text = _("No tax set on the account move line!")
                error_text += " " + str(account_move_line_details)
                error_list.append(error_text)
            else:
                pass
        else:
            pass

        # Check invoice_line_values TODO
        if invoice_line_values:
            line_tax_set.update({
                'invoice_line_values_result': 'error'
            })
        else:
            pass

        # Check invoice_line
        if invoice_line:
            if invoice_line.account_tax:
                line_tax_set.update({
                    'invoice_line_result': 'ok',
                    'invoice_line_value': invoice_line.account_tax,
                })
                success_text = _("There is a tax set on the invoice line.")
                success_text += " " + str(invoice_line_details)
                success_list.append(success_text)
            else:
                line_tax_set.update({
                    'invoice_line_result': 'error',
                    'invoice_line_value': False,
                })
                error_text = _("No tax set on the invoice line!")
                error_text += " " + str(invoice_line_details)
                error_list.append(error_text)
        else:
            pass

        if account_move_line and invoice_line:
            if line_tax_set['account_move_line_result'] == line_tax_set['invoice_line_result']:
                success_list.append(_("TAX set ok"))

        # Append to healthcheck_results
        healthcheck_results.append(line_tax_set)

        # 02) line_tax_l10n_hu
        line_tax_l10n_hu = {
            'category': 'invoice_line',
            'description': _("There must be exactly one HU tax set on the line"),
            'name': _("Invoice line HU tax"),
            'technical_name': 'line_tax_l10n_hu',
        }

        # Check line display_type
        if account_move \
                and not account_move.l10n_hu_eu_oss_eligible \
                and account_move_line \
                and account_move_line.display_type not in ['line_note', 'line_section']:
            if account_move_line.tax_ids and len(account_move_line.tax_ids) == 1:
                if account_move_line.tax_ids[0].l10n_hu_vat_enabled:
                    line_tax_l10n_hu.update({
                        'account_move_line_result': 'ok',
                        'account_move_line_value': account_move_line.tax_ids[0].l10n_hu_vat_enabled,
                    })
                    success_text = _("There is one tax set on the account move line and it is HU VAT tax.")
                    success_text += " " + str(account_move_line_details)
                    success_list.append(success_text)
                else:
                    line_tax_l10n_hu.update({
                        'account_move_line_result': 'error',
                        'account_move_line_value': False,
                    })
                    error_text = _("The tax set on the account move line is not HU VAT tax!")
                    error_text += " " + str(account_move_line_details)
                    error_list.append(error_text)
            # We already checked existence and count of tax in 01 check
            # So no need to duplicate error list, but still set result to failure so that final comparison works
            else:
                line_tax_l10n_hu.update({
                    'account_move_line_result': 'error',
                    'account_move_line_value': account_move_line.tax_ids,
                })
        else:
            pass

        # Check invoice_line_values TODO
        if invoice_line_values:
            line_tax_l10n_hu.update({
                'invoice_line_values_result': 'error',
            })
        else:
            pass

        # Check invoice_line
        if invoice_line:
            if invoice_line.account_tax and invoice_line.account_tax.l10n_hu_vat_enabled:
                line_tax_l10n_hu.update({
                    'invoice_line_result': 'ok',
                    'invoice_line_value': invoice_line.account_tax.l10n_hu_vat_enabled,
                })
                success_text = _("The tax on the invoice line is HU VAT tax.")
                success_text += " " + str(invoice_line_details)
                success_list.append(success_text)
            elif invoice_line.account_tax:
                line_tax_l10n_hu.update({
                    'invoice_line_result': 'error',
                    'invoice_line_value': False,
                })
                error_text = _("The tax set on the invoice line is not HU VAT tax.")
                error_text += " " + str(invoice_line_details)
                error_list.append(error_text)
            else:
                line_tax_l10n_hu.update({
                    'invoice_line_result': 'error',
                })
                # We already checked existence of tax in check 01, no need to add more error messages
        else:
            pass

        if account_move_line and invoice_line:
            if line_tax_l10n_hu['account_move_line_result'] == line_tax_l10n_hu['invoice_line_result']:
                success_list.append(_("HU VAT ok"))

        # Append to healthcheck_results
        healthcheck_results.append(line_tax_l10n_hu)

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'healthcheck_results': healthcheck_results,
            'info_list': info_list,
            'success_list': success_list,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result

    @api.model
    def run_healthcheck_invoice_summary(self):
        """ Run healthcheck on the summary of an invoice

        TODO: expand checklist

        :return: dictionary
        """
        # raise exceptions.UserError(str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # Update result
        if len(error_list) == 0:
            result.update({
                'debug_list': debug_list,
                'description': "OK",
                'error_list': error_list,
                'info_list': info_list,
                'type': 'success',
                'warning_list': warning_list,
            })
        else:
            result.update({
                'debug_list': debug_list,
                'description': "Completed with errors",
                'error_list': error_list,
                'info_list': info_list,
                'type': 'error',
                'warning_list': warning_list,
            })

        # Return result
        # raise exceptions.UserError(str(result))
        return result

    @api.model
    def run_healthcheck_system(self):
        """ Run healthcheck on the system

        TODO: expand checklist

        :return: dictionary
        """
        # raise exceptions.UserError(str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # Update result
        if len(error_list) == 0:
            result.update({
                'debug_list': debug_list,
                'description': "OK",
                'error_list': error_list,
                'info_list': info_list,
                'type': 'success',
                'warning_list': warning_list,
            })
        else:
            result.update({
                'debug_list': debug_list,
                'description': "Completed with errors",
                'error_list': error_list,
                'info_list': info_list,
                'type': 'error',
                'warning_list': warning_list,
            })

        # Return result
        # raise exceptions.UserError(str(result))
        return result

    @api.model
    def run_invoice_maintenance(self, values):
        """ Run maintenance on an invoice

        NOTE:
        - wrapper method
        - performs write
        - other operations are to be executed using the run_invoice_maintenance_operations method

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("run_invoice_maintenance BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []
        write_values = {}

        # Set invoice
        if values.get('invoice'):
            invoice = values['invoice']
            debug_list.append("invoice found in values: " + str(invoice))
        elif len(self) == 1 and self.id:
            invoice = self
            debug_list.append("using self as invoice: " + str(self))
        else:
            invoice = False
            error_list.append("could not set invoice")

        # Pull from account move as part of maintenance
        operations_result = invoice.run_invoice_maintenance_operations({})
        operations = operations_result.get('operations', [])

        # Lists
        debug_list += operations_result['debug_list']
        error_list += operations_result['error_list']
        info_list += operations_result['info_list']
        warning_list += operations_result['warning_list']

        # maintenance_status
        if len(error_list) == 0:
            maintenance_status = 'done'
        else:
            maintenance_status = 'error'

        # write
        if invoice:
            maintenance_data = {
                'error_list': error_list,
                'info_list': info_list,
                'operations': operations,
                'warning_list': warning_list,
            }
            write_values.update({
                'maintenance_data': json.dumps(maintenance_data, default=str),
                'maintenance_status': maintenance_status,
                'maintenance_timestamp': fields.Datetime.now(),
            })
            invoice.sudo().write(write_values)

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'maintenance_status': maintenance_status,
            'invoice': invoice,
            'operations': operations,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("run_invoice_maintenance END" + str(result))
        return result

    @api.model
    def run_invoice_maintenance_operations(self, values):
        """ Run maintenance operations on an invoice

        NOTE:
        - called from a wrapper method, should not be called directly elsewhere
        - can be overridden by super

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("run_invoice_maintenance_operations BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        operations = []
        result = {}
        warning_list = []

        # Set invoice
        if values.get('invoice'):
            invoice = values['invoice']
            debug_list.append("invoice found in values: " + str(invoice))
        elif len(self) == 1 and self.id:
            invoice = self
            debug_list.append("using self as invoice: " + str(self))
        else:
            invoice = False
            error_list.append("could not set invoice")

        # Pull from account move as part of maintenance
        if invoice \
                and invoice.account_journal.type in ['purchase', 'sale'] \
                and invoice.account_move\
                and not invoice.is_locked:
            invoice.pull_from_account_move()
            operations.append("pull_from_account_move")
            info_list.append("pull_from_account_move executed")

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'invoice': invoice,
            'operations': operations,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("run_invoice_maintenance_operations END" + str(result))
        return result
