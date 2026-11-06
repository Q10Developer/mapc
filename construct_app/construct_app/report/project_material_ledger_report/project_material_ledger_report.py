# Copyright (c) 2026, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	validate_filters(filters)

	party_field = {"Supplier": "supplier", "Contractor": "contractor"}[filters.party_type]
	party_value = filters.get(party_field)
	if not party_value:
		frappe.throw(_("Please select a {0}.").format(_(filters.party_type)))

	rows = frappe.db.sql(
		f"""
		SELECT
			material_code,
			material_description,
			challan_invoice_no,
			receipt_date,
			invoice_qty,
			actual_qty,
			uom,
			rate,
			COALESCE(NULLIF(amount, 0), actual_qty * rate, 0) AS amount
		FROM `tabProject Material Ledger`
		WHERE project = %(project)s
			AND party_type = %(party_type)s
			AND {party_field} = %(party)s
			AND receipt_date BETWEEN %(from_date)s AND %(to_date)s
		ORDER BY receipt_date ASC, challan_invoice_no ASC, name ASC
		""",
		{
			"project": filters.project,
			"party_type": filters.party_type,
			"party": party_value,
			"from_date": filters.from_date,
			"to_date": filters.to_date,
		},
		as_dict=True,
	)

	data = list(rows)
	total_row = {
		"material_code": _("Total"),
		"invoice_qty": sum(flt(row.invoice_qty) for row in rows),
		"actual_qty": sum(flt(row.actual_qty) for row in rows),
		"amount": sum(flt(row.amount) for row in rows),
		"bold": 1,
	}
	data.append(total_row)

	return get_columns(), data


def validate_filters(filters):
	for fieldname in ("project", "party_type", "from_date", "to_date"):
		if not filters.get(fieldname):
			frappe.throw(_("Please select {0}.").format(_(fieldname.replace("_", " ").title())))

	if filters.party_type not in ("Supplier", "Contractor"):
		frappe.throw(_("Party Type must be Supplier or Contractor."))

	if getdate(filters.from_date) > getdate(filters.to_date):
		frappe.throw(_("From Date cannot be later than To Date."))


def get_columns():
	return [
		{"label": _("Material Code"), "fieldname": "material_code", "fieldtype": "Data", "width": 140},
		{
			"label": _("Material Description"),
			"fieldname": "material_description",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": _("Challan/Invoice No"),
			"fieldname": "challan_invoice_no",
			"fieldtype": "Data",
			"width": 160,
		},
		{"label": _("Receipt Date"), "fieldname": "receipt_date", "fieldtype": "Date", "width": 110},
		{"label": _("Invoice Qty"), "fieldname": "invoice_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Actual Qty"), "fieldname": "actual_qty", "fieldtype": "Float", "width": 110},
		{"label": _("UOM"), "fieldname": "uom", "fieldtype": "Link", "options": "UOM", "width": 90},
		{"label": _("Rate"), "fieldname": "rate", "fieldtype": "Currency", "width": 110},
		{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 120},
	]
