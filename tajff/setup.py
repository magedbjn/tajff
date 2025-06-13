import os

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.desk.page.setup_wizard.install_fixtures import (
	_,  # NOTE: this is not the real translation function
)
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.installer import update_site_config


def after_install():
	create_custom_fields(get_custom_fields(), ignore_validate=True)


def before_uninstall():
	delete_custom_fields(get_custom_fields())


def get_custom_fields():
	"""Tajff specific custom fields that need to be added to the masters in ERPNext"""
	return {
		"Leave Application": [
		{
			"fieldname": "custom_overlapping_days_compensated",
			"label": "Overlapping Days Compensated with Public Holidays",
			"fieldtype": "Int",
			"insert_after": "to_date",
			"read_only": 1,
			"depends_on": "eval:doc.custom_overlapping_days_compensated!=0",
		},
		{
			"fieldname": "custom_travel",
			"label": "Travel",
			"fieldtype": "Tab Break",
			"insert_after": "amended_from",
		},
		{
			"fieldname": "custom_travel_ticket",
			"label": "Travel Ticket",
			"fieldtype": "Check",
			"default": 0,
			"insert_after": "custom_travel",
		},
		{
			"fieldname": "custom_last_travel_ticket",
			"label": "Last Travel Ticket",
			"fieldtype": "Read Only",
			"insert_after": "custom_travel_ticket",
		},
		{
			"fieldname": "custom_status_travel_ticket",
			"label": "Status Travel Ticket",
			"fieldtype": "Select",
			"insert_after": "custom_travel_ticket",
			"options": "\nCovered by company\nReimbursable Expense\nNon-Reimbursable Expense",
			"read_only_depends_on": "eval:doc.custom_travel_ticket==0",
		},
		{
			"fieldname": "custom_column_break_mhfpk",
			"label": "",
			"fieldtype": "Column Break",
			"insert_after": "custom_status_travel_ticket",
		},
		{
			"fieldname": "custom_return_visa",
			"label": "Return Visa",
			"fieldtype": "Check",
			"default": 0,
			"insert_after": "custom_column_break_mhfpk",
		},
		{
			"fieldname": "custom_last_return_visa",
			"label": "Last Return Visa",
			"fieldtype": "Read Only",
			"insert_after": "custom_return_visa",
		},
		{
			"fieldname": "custom_last_return_visa",
			"label": "Status Return Visa",
			"fieldtype": "Select",
			"insert_after": "custom_return_visa",
			"options": "\nCovered by company\nReimbursable Expense\nNon-Reimbursable Expense",
			"read_only_depends_on": "eval:doc.custom_return_visa==0",
		}
	]
}




	docperms = data.get("doctypes")
	if doc.role == "Employee Self Service" and "lending" in frappe.get_installed_apps():
		docperms.update(get_lending_docperms_for_ess())

	append_docperms_to_user_type(docperms, doc)

	doc.flags.ignore_links = True
	doc.save(ignore_permissions=True)


def delete_custom_fields(custom_fields: dict):
	"""
	:param custom_fields: a dict like `{'Leave Application': [{fieldname: 'Travels', ...}]}`
	"""
	for doctype, fields in custom_fields.items():
		frappe.db.delete(
			"Custom Field",
			{
				"fieldname": ("in", [field["fieldname"] for field in fields]),
				"dt": doctype,
			},
		)

		frappe.clear_cache(doctype=doctype)
